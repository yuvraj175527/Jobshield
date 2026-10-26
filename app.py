from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from flask_bcrypt import Bcrypt

from database.db_connection import get_db_connection
from utils.hybrid_analyzer import analyze_job_hybrid

import random
import smtplib

from email.message import EmailMessage

from datetime import datetime, timedelta


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "jobshield_secret_key_change_this"

bcrypt = Bcrypt(app)


# =========================================================
# EMAIL CONFIGURATION
# =========================================================
#
# IMPORTANT:
# Use a Gmail App Password.
# DO NOT use your normal Gmail password.
#
# Example:
#
# MAIL_SENDER = "jobshieldproject@gmail.com"
# MAIL_PASSWORD = "abcdefghijklmnop"
#
# =========================================================

MAIL_SENDER = "jobshield46@gmail.com"
MAIL_PASSWORD = "rmhk swes yanj utvw"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template("index.html")


# =========================================================
# USER REGISTRATION
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        if not name or not email or not password:

            flash(
                "Please fill in all required fields.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        if len(password) < 8:

            flash(
                "Password must contain at least 8 characters.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        try:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            existing_user = cursor.fetchone()


            if existing_user:

                flash(
                    "An account with this email already exists.",
                    "danger"
                )

                return redirect(
                    url_for("register")
                )


            hashed_password = (
                bcrypt
                .generate_password_hash(password)
                .decode("utf-8")
            )


            cursor.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password,
                    role
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    'user'
                )
                """,
                (
                    name,
                    email,
                    hashed_password
                )
            )


            connection.commit()


            flash(
                "Registration successful. Please login.",
                "success"
            )


            return redirect(
                url_for("login")
            )


        finally:

            cursor.close()
            connection.close()


    return render_template(
        "register.html"
    )


# =========================================================
# USER LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        try:

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()


        finally:

            cursor.close()
            connection.close()


        if user and bcrypt.check_password_hash(
            user["password"],
            password
        ):


            if user["role"] == "admin":

                flash(
                    "Administrator accounts must use Admin Login.",
                    "warning"
                )

                return redirect(
                    url_for("admin_login")
                )


            session.clear()


            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["role"] = "user"


            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "login.html"
    )


# =========================================================
# SEND PASSWORD RESET OTP
# =========================================================

def send_reset_otp(
    receiver_email,
    otp
):

    message = EmailMessage()


    message["Subject"] = (
        "JobShield Password Reset OTP"
    )


    message["From"] = MAIL_SENDER


    message["To"] = receiver_email


    message.set_content(
        f"""
Hello,

We received a request to reset your JobShield account password.

Your password reset OTP is:

{otp}

This OTP is valid for 10 minutes.

If you did not request a password reset, you can safely ignore this email.

Regards,
JobShield
Fake Job Detection & Verification System
"""
    )


    # Gmail SMTP
    # Port 587 with STARTTLS

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as smtp:

        smtp.ehlo()

        smtp.starttls()

        smtp.ehlo()

        smtp.login(
            MAIL_SENDER,
            MAIL_PASSWORD
        )

        smtp.send_message(
            message
        )


# =========================================================
# FORGOT PASSWORD
# =========================================================

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()


        if not email:

            flash(
                "Please enter your email address.",
                "danger"
            )

            return redirect(
                url_for("forgot_password")
            )


        # -------------------------------------------------
        # FIND USER
        # -------------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        try:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    email
                FROM users
                WHERE email = %s
                AND role = 'user'
                """,
                (email,)
            )

            user = cursor.fetchone()


        finally:

            cursor.close()
            connection.close()


        if not user:

            flash(
                "No JobShield account was found with this email address.",
                "danger"
            )

            return redirect(
                url_for("forgot_password")
            )


        # -------------------------------------------------
        # GENERATE 6 DIGIT OTP
        # -------------------------------------------------

        otp = str(
            random.randint(
                100000,
                999999
            )
        )


        # OTP expires after 10 minutes

        expires_at = (
            datetime.now()
            + timedelta(
                minutes=10
            )
        )


        # -------------------------------------------------
        # SAVE OTP
        # -------------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor()


        try:

            # Delete previous OTPs

            cursor.execute(
                """
                DELETE FROM password_resets
                WHERE user_id = %s
                """,
                (user["id"],)
            )


            # Insert new OTP

            cursor.execute(
                """
                INSERT INTO password_resets
                (
                    user_id,
                    otp,
                    expires_at
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    user["id"],
                    otp,
                    expires_at
                )
            )


            connection.commit()


        finally:

            cursor.close()
            connection.close()


        # -------------------------------------------------
        # SEND OTP EMAIL
        # -------------------------------------------------

        try:

            send_reset_otp(
                user["email"],
                otp
            )


        except Exception as e:

            print(
                "========================================"
            )

            print(
                "PASSWORD RESET EMAIL ERROR:"
            )

            print(
                repr(e)
            )

            print(
                "========================================"
            )


            # Delete OTP because email failed

            connection = get_db_connection()

            cursor = connection.cursor()


            try:

                cursor.execute(
                    """
                    DELETE FROM password_resets
                    WHERE user_id = %s
                    """,
                    (user["id"],)
                )

                connection.commit()


            finally:

                cursor.close()
                connection.close()


            flash(
                "Unable to send the verification code. Please check your email configuration.",
                "danger"
            )

            return redirect(
                url_for("forgot_password")
            )


        # -------------------------------------------------
        # SAVE RESET SESSION
        # -------------------------------------------------

        session["reset_user_id"] = user["id"]

        session["reset_email"] = user["email"]


        flash(
            "A verification code has been sent to your email.",
            "success"
        )


        return redirect(
            url_for("verify_otp")
        )


    return render_template(
        "forgot_password.html"
    )


# =========================================================
# VERIFY OTP
# =========================================================

@app.route(
    "/verify-otp",
    methods=["GET", "POST"]
)
def verify_otp():

    if "reset_user_id" not in session:

        return redirect(
            url_for("forgot_password")
        )


    if request.method == "POST":

        otp = request.form.get(
            "otp",
            ""
        ).strip()


        if not otp:

            flash(
                "Please enter the verification code.",
                "danger"
            )

            return redirect(
                url_for("verify_otp")
            )


        if (
            not otp.isdigit()
            or len(otp) != 6
        ):

            flash(
                "Please enter a valid 6-digit OTP.",
                "danger"
            )

            return redirect(
                url_for("verify_otp")
            )


        # -------------------------------------------------
        # FIND OTP
        # -------------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        try:

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    otp,
                    expires_at
                FROM password_resets
                WHERE user_id = %s
                AND otp = %s
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (
                    session["reset_user_id"],
                    otp
                )
            )


            reset_record = cursor.fetchone()


        finally:

            cursor.close()
            connection.close()


        # -------------------------------------------------
        # INVALID OTP
        # -------------------------------------------------

        if not reset_record:

            flash(
                "Invalid verification code.",
                "danger"
            )

            return redirect(
                url_for("verify_otp")
            )


        # -------------------------------------------------
        # CHECK OTP EXPIRATION
        # -------------------------------------------------

        if datetime.now() > reset_record["expires_at"]:

            connection = get_db_connection()

            cursor = connection.cursor()


            try:

                cursor.execute(
                    """
                    DELETE FROM password_resets
                    WHERE id = %s
                    """,
                    (reset_record["id"],)
                )

                connection.commit()


            finally:

                cursor.close()
                connection.close()


            flash(
                "This verification code has expired. Please request a new one.",
                "danger"
            )

            return redirect(
                url_for("forgot_password")
            )


        # -------------------------------------------------
        # OTP VERIFIED
        # -------------------------------------------------

        session["otp_verified"] = True


        return redirect(
            url_for("reset_password")
        )


    return render_template(
        "verify_otp.html",
        email=session.get(
            "reset_email"
        )
    )


# =========================================================
# RESET PASSWORD
# =========================================================

@app.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():

    if "reset_user_id" not in session:

        return redirect(
            url_for("forgot_password")
        )


    if not session.get(
        "otp_verified"
    ):

        return redirect(
            url_for("verify_otp")
        )


    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )


        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        # -------------------------------------------------
        # VALIDATE
        # -------------------------------------------------

        if (
            not password
            or not confirm_password
        ):

            flash(
                "Please fill in both password fields.",
                "danger"
            )

            return redirect(
                url_for("reset_password")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("reset_password")
            )


        if len(password) < 8:

            flash(
                "Password must contain at least 8 characters.",
                "danger"
            )

            return redirect(
                url_for("reset_password")
            )


        # -------------------------------------------------
        # HASH PASSWORD
        # -------------------------------------------------

        hashed_password = (
            bcrypt
            .generate_password_hash(
                password
            )
            .decode("utf-8")
        )


        # -------------------------------------------------
        # UPDATE DATABASE
        # -------------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor()


        try:

            cursor.execute(
                """
                UPDATE users
                SET password = %s
                WHERE id = %s
                """,
                (
                    hashed_password,
                    session["reset_user_id"]
                )
            )


            # Delete used OTP

            cursor.execute(
                """
                DELETE FROM password_resets
                WHERE user_id = %s
                """,
                (
                    session["reset_user_id"],
                )
            )


            connection.commit()


        finally:

            cursor.close()
            connection.close()


        # -------------------------------------------------
        # CLEAR RESET SESSION
        # -------------------------------------------------

        session.pop(
            "reset_user_id",
            None
        )

        session.pop(
            "reset_email",
            None
        )

        session.pop(
            "otp_verified",
            None
        )


        flash(
            "Your password has been reset successfully. Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "reset_password.html"
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()


        password = request.form.get(
            "password",
            ""
        )


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        try:

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email = %s
                AND role = 'admin'
                """,
                (email,)
            )

            admin = cursor.fetchone()


        finally:

            cursor.close()
            connection.close()


        if admin and bcrypt.check_password_hash(
            admin["password"],
            password
        ):

            session.clear()


            session["user_id"] = admin["id"]

            session["user_name"] = admin["name"]

            session["role"] = "admin"


            return redirect(
                url_for("admin_dashboard")
            )


        flash(
            "Invalid administrator credentials.",
            "danger"
        )


    return render_template(
        "admin/login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# USER DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin_dashboard")
        )


    user_id = session["user_id"]


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        cursor.execute(
            """
            SELECT COUNT(*) AS total_jobs
            FROM jobs
            WHERE user_id = %s
            """,
            (user_id,)
        )


        total_jobs = cursor.fetchone()[
            "total_jobs"
        ]


        cursor.execute(
            """
            SELECT COUNT(*) AS high_risk_jobs
            FROM jobs j
            JOIN verifications v
            ON j.id = v.job_id
            WHERE j.user_id = %s
            AND v.risk_level = 'High Risk'
            """,
            (user_id,)
        )


        high_risk_jobs = cursor.fetchone()[
            "high_risk_jobs"
        ]


        cursor.execute(
            """
            SELECT COUNT(*) AS suspicious_jobs
            FROM jobs j
            JOIN verifications v
            ON j.id = v.job_id
            WHERE j.user_id = %s
            AND v.risk_level = 'Suspicious'
            """,
            (user_id,)
        )


        suspicious_jobs = cursor.fetchone()[
            "suspicious_jobs"
        ]


    finally:

        cursor.close()
        connection.close()


    return render_template(
        "dashboard.html",

        total_jobs=total_jobs,

        high_risk_jobs=high_risk_jobs,

        suspicious_jobs=suspicious_jobs
    )


# =========================================================
# VERIFY JOB
# =========================================================

@app.route(
    "/verify-job",
    methods=["GET", "POST"]
)
def verify_job():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin_dashboard")
        )


    if request.method == "POST":

        company_name = request.form.get(
            "company_name",
            ""
        ).strip()


        job_title = request.form.get(
            "job_title",
            ""
        ).strip()


        recruiter_name = request.form.get(
            "recruiter_name",
            ""
        ).strip()


        job_url = request.form.get(
            "job_url",
            ""
        ).strip()


        salary = request.form.get(
            "salary",
            ""
        ).strip()


        description = request.form.get(
            "description",
            ""
        ).strip()


        if (
            not company_name
            or not job_title
            or not description
        ):

            flash(
                "Company name, job title and description are required.",
                "danger"
            )

            return redirect(
                url_for("verify_job")
            )


        # -------------------------------------------------
        # HYBRID ANALYSIS
        # -------------------------------------------------

        result = analyze_job_hybrid(
            company_name=company_name,
            job_title=job_title,
            recruiter_name=recruiter_name,
            job_url=job_url,
            salary=salary,
            description=description
        )


        connection = get_db_connection()

        cursor = connection.cursor()


        try:

            # Insert job

            cursor.execute(
                """
                INSERT INTO jobs
                (
                    user_id,
                    company_name,
                    job_title,
                    recruiter_name,
                    job_url,
                    salary,
                    description
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    session["user_id"],
                    company_name,
                    job_title,
                    recruiter_name,
                    job_url,
                    salary,
                    description
                )
            )


            job_id = cursor.lastrowid


            # Insert verification

            cursor.execute(
                """
                INSERT INTO verifications
                (
                    job_id,
                    risk_score,
                    risk_level,
                    status,
                    reasons
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    job_id,
                    result["risk_score"],
                    result["risk_level"],
                    result["status"],
                    "\n".join(
                        result["reasons"]
                    )
                )
            )


            connection.commit()


        finally:

            cursor.close()
            connection.close()


        return render_template(
            "verification_result.html",

            job_id=job_id,

            company_name=company_name,

            job_title=job_title,

            recruiter_name=recruiter_name,

            job_url=job_url,

            salary=salary,

            description=description,

            risk_score=result["risk_score"],

            risk_level=result["risk_level"],

            status=result["status"],

            reasons=result["reasons"],

            rule_score=result.get(
                "rule_score",
                0
            ),

            ml_fake_probability=result.get(
                "ml_fake_probability",
                0
            ),

            ml_genuine_probability=result.get(
                "ml_genuine_probability",
                0
            ),

            ml_threshold=result.get(
                "ml_threshold",
                0.70
            )
        )


    return render_template(
        "verify_job.html"
    )


# =========================================================
# VERIFICATION HISTORY
# =========================================================

@app.route(
    "/verification-history"
)
def verification_history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin_dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        cursor.execute(
            """
            SELECT

                j.id,

                j.company_name,

                j.job_title,

                j.recruiter_name,

                j.job_url,

                j.salary,

                j.created_at,

                v.risk_score,

                v.risk_level,

                v.status,

                v.reasons,

                v.verified_at

            FROM jobs j

            LEFT JOIN verifications v
            ON j.id = v.job_id

            WHERE j.user_id = %s

            ORDER BY j.created_at DESC
            """,
            (
                session["user_id"],
            )
        )


        jobs = cursor.fetchall()


    finally:

        cursor.close()
        connection.close()


    return render_template(
        "verification_history.html",
        jobs=jobs
    )


# =========================================================
# REPORT A FAKE JOB
# =========================================================

@app.route(
    "/report-job",
    methods=["GET", "POST"]
)
def report_job():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin_dashboard")
        )


    if request.method == "POST":

        job_id = request.form.get(
            "job_id",
            ""
        ).strip()


        reason = request.form.get(
            "reason",
            ""
        ).strip()


        description = request.form.get(
            "description",
            ""
        ).strip()


        if (
            not reason
            or not description
        ):

            flash(
                "Please provide a reason and report details.",
                "danger"
            )

            return redirect(
                url_for("report_job")
            )


        if job_id == "":

            job_id = None


        else:

            try:

                job_id = int(
                    job_id
                )


            except ValueError:

                flash(
                    "Invalid Job ID.",
                    "danger"
                )

                return redirect(
                    url_for("report_job")
                )


        connection = get_db_connection()

        cursor = connection.cursor()


        try:

            cursor.execute(
                """
                INSERT INTO reports
                (
                    user_id,
                    job_id,
                    reason,
                    description,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    'Pending'
                )
                """,
                (
                    session["user_id"],
                    job_id,
                    reason,
                    description
                )
            )


            connection.commit()


        finally:

            cursor.close()
            connection.close()


        flash(
            "Your report has been submitted successfully.",
            "success"
        )


        return redirect(
            url_for("reports")
        )


    return render_template(
        "report_job.html"
    )


# =========================================================
# MY REPORTS
# =========================================================

@app.route("/reports")
def reports():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin_dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        cursor.execute(
            """
            SELECT

                r.id,

                r.reason,

                r.description,

                r.status,

                r.reported_at,

                j.company_name,

                j.job_title

            FROM reports r

            LEFT JOIN jobs j
            ON r.job_id = j.id

            WHERE r.user_id = %s

            ORDER BY r.reported_at DESC
            """,
            (
                session["user_id"],
            )
        )


        reports_data = cursor.fetchall()


    finally:

        cursor.close()
        connection.close()


    return render_template(
        "reports.html",
        reports=reports_data
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin_dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("admin_login")
        )


    if session.get("role") != "admin":

        return redirect(
            url_for("dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        cursor.execute(
            """
            SELECT COUNT(*) AS total_users
            FROM users
            WHERE role = 'user'
            """
        )


        total_users = cursor.fetchone()[
            "total_users"
        ]


        cursor.execute(
            """
            SELECT COUNT(*) AS total_jobs
            FROM jobs
            """
        )


        total_jobs = cursor.fetchone()[
            "total_jobs"
        ]


        cursor.execute(
            """
            SELECT COUNT(*) AS total_reports
            FROM reports
            """
        )


        total_reports = cursor.fetchone()[
            "total_reports"
        ]


        cursor.execute(
            """
            SELECT COUNT(*) AS pending_reports
            FROM reports
            WHERE status = 'Pending'
            """
        )


        pending_reports = cursor.fetchone()[
            "pending_reports"
        ]


        cursor.execute(
            """
            SELECT COUNT(*) AS resolved_reports
            FROM reports
            WHERE status = 'Resolved'
            """
        )


        resolved_reports = cursor.fetchone()[
            "resolved_reports"
        ]


    finally:

        cursor.close()
        connection.close()


    return render_template(
        "admin/dashboard.html",

        total_users=total_users,

        total_jobs=total_jobs,

        total_reports=total_reports,

        pending_reports=pending_reports,

        resolved_reports=resolved_reports
    )


# =========================================================
# ADMIN USERS
# =========================================================

@app.route("/admin/users")
def admin_users():

    if "user_id" not in session:

        return redirect(
            url_for("admin_login")
        )


    if session.get("role") != "admin":

        return redirect(
            url_for("dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        cursor.execute(
            """
            SELECT

                id,

                name,

                email,

                role,

                created_at

            FROM users

            ORDER BY created_at DESC
            """
        )


        users = cursor.fetchall()


    finally:

        cursor.close()
        connection.close()


    return render_template(
        "admin/users.html",
        users=users
    )


# =========================================================
# ADMIN JOBS
# =========================================================

@app.route("/admin/jobs")
def admin_jobs():

    if "user_id" not in session:

        return redirect(
            url_for("admin_login")
        )


    if session.get("role") != "admin":

        return redirect(
            url_for("dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        cursor.execute(
            """
            SELECT

                j.id,

                j.company_name,

                j.job_title,

                j.recruiter_name,

                j.job_url,

                j.salary,

                j.created_at,

                u.name AS user_name,

                u.email AS user_email,

                v.risk_score,

                v.risk_level,

                v.status,

                v.reasons,

                v.verified_at

            FROM jobs j

            LEFT JOIN users u
            ON j.user_id = u.id

            LEFT JOIN verifications v
            ON j.id = v.job_id

            ORDER BY j.created_at DESC
            """
        )


        jobs = cursor.fetchall()


    finally:

        cursor.close()
        connection.close()


    return render_template(
        "admin/jobs.html",
        jobs=jobs
    )


# =========================================================
# ADMIN REPORTS
# =========================================================

@app.route("/admin/reports")
def admin_reports():

    if "user_id" not in session:

        return redirect(
            url_for("admin_login")
        )


    if session.get("role") != "admin":

        return redirect(
            url_for("dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        cursor.execute(
            """
            SELECT

                r.id,

                r.user_id,

                r.job_id,

                r.reason,

                r.description,

                r.status,

                r.reported_at,

                u.name AS user_name,

                u.email AS user_email,

                j.company_name,

                j.job_title

            FROM reports r

            LEFT JOIN users u
            ON r.user_id = u.id

            LEFT JOIN jobs j
            ON r.job_id = j.id

            ORDER BY r.reported_at DESC
            """
        )


        reports_data = cursor.fetchall()


    finally:

        cursor.close()
        connection.close()


    return render_template(
        "admin/reports.html",
        reports=reports_data
    )


# =========================================================
# ADMIN UPDATE REPORT STATUS
# =========================================================

@app.route(
    "/admin/reports/<int:report_id>/status",
    methods=["POST"]
)
def update_report_status(
    report_id
):

    if "user_id" not in session:

        return redirect(
            url_for("admin_login")
        )


    if session.get("role") != "admin":

        return redirect(
            url_for("dashboard")
        )


    new_status = request.form.get(
        "status",
        ""
    ).strip()


    allowed_statuses = [
        "Pending",
        "Under Review",
        "Resolved",
        "Rejected"
    ]


    if new_status not in allowed_statuses:

        flash(
            "Invalid report status.",
            "danger"
        )

        return redirect(
            url_for("admin_reports")
        )


    connection = get_db_connection()

    cursor = connection.cursor()


    try:

        cursor.execute(
            """
            UPDATE reports

            SET status = %s

            WHERE id = %s
            """,
            (
                new_status,
                report_id
            )
        )


        connection.commit()


    finally:

        cursor.close()
        connection.close()


    flash(
        f"Report #{report_id} status updated to {new_status}.",
        "success"
    )


    return redirect(
        url_for("admin_reports")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )