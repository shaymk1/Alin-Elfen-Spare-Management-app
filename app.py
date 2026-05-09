from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from flask import Flask, flash, g, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "change-me-before-production"
PER_PAGE = 8


@dataclass
class User:
    id: int
    username: str
    email: Optional[str]
    role: str
    created_at: datetime
    is_active: bool = True
    password: str = ""


@dataclass
class Spare:
    id: int
    name: str
    description: Optional[str]
    part_number: Optional[str]
    item_type: str
    quantity_in_stock: int
    minimum_quantity: int
    unit: Optional[str]
    location: Optional[str]


@dataclass
class BorrowRecord:
    id: int
    spare: Spare
    quantity: int
    borrowed_by: User
    borrowed_at: datetime
    expected_return_date: Optional[datetime]
    is_returned: bool = False


@dataclass
class ReturnRecord:
    id: int
    borrow_record: BorrowRecord
    quantity_returned: int
    condition: Optional[str]
    returned_by: User
    returned_at: datetime
    notes: Optional[str]


@dataclass
class AuditLogEntry:
    id: int
    timestamp: datetime
    action: str
    entity_type: str
    entity_id: Optional[int]
    performed_by: Optional[User]
    ip_address: Optional[str]
    changes: Optional[str]


class Pagination:
    def __init__(self, items: List, page: int, per_page: int = PER_PAGE):
        self.page = max(1, page)
        self.per_page = per_page
        self.total = len(items)
        self.pages = max(1, (self.total + per_page - 1) // per_page)
        start = (self.page - 1) * per_page
        end = start + per_page
        self.items = items[start:end]
        self.has_prev = self.page > 1
        self.has_next = self.page < self.pages
        self.prev_num = max(1, self.page - 1)
        self.next_num = min(self.pages, self.page + 1)

    def iter_pages(self):
        return range(1, self.pages + 1)


users: List[User] = [
    User(
        1, "admin", "admin@example.com", "admin", datetime(2026, 1, 1), True, "admin123"
    ),
    User(
        2,
        "store_manager",
        "store@example.com",
        "store_manager",
        datetime(2026, 2, 1),
        True,
        "manager123",
    ),
    User(
        3,
        "general_manager",
        "gm@example.com",
        "general_manager",
        datetime(2026, 3, 1),
        True,
        "gm123",
    ),
]

spares: List[Spare] = [
    Spare(
        1,
        "Industrial Wrench",
        "Heavy-duty adjustable wrench.",
        "WRC-001",
        "reusable",
        28,
        10,
        "pcs",
        "Shelf A1",
    ),
    Spare(
        2,
        "Safety Gloves",
        "Pair of protective gloves.",
        "GLV-009",
        "consumable",
        14,
        5,
        "pairs",
        "Rack B2",
    ),
    Spare(
        3,
        "Electrical Tape",
        "Insulating tape.",
        "TPE-015",
        "consumable",
        3,
        5,
        "rolls",
        "Shelf C3",
    ),
    Spare(
        4,
        "Hydraulic Pump",
        "Portable hydraulic pump.",
        "HPP-102",
        "reusable",
        2,
        1,
        "units",
        "Cabinet D4",
    ),
    Spare(
        5,
        "Replacement Fuse",
        "10A automotive fuse.",
        "FSE-010",
        "consumable",
        0,
        5,
        "pcs",
        "Tray E5",
    ),
]

borrow_records: List[BorrowRecord] = [
    BorrowRecord(
        1,
        spares[0],
        1,
        users[1],
        datetime.now() - timedelta(days=4, hours=2),
        datetime.now() + timedelta(days=3),
        False,
    ),
    BorrowRecord(
        2,
        spares[3],
        1,
        users[2],
        datetime.now() - timedelta(days=10),
        datetime.now() - timedelta(days=2),
        True,
    ),
]

return_records: List[ReturnRecord] = [
    ReturnRecord(
        1,
        borrow_records[1],
        1,
        "good",
        users[2],
        datetime.now() - timedelta(days=3),
        "Returned after inspection.",
    )
]

fair_audit: List[AuditLogEntry] = [
    AuditLogEntry(
        1,
        datetime.now() - timedelta(days=7),
        "add",
        "spare",
        1,
        users[1],
        "127.0.0.1",
        "Created Industrial Wrench with 28 units.",
    ),
    AuditLogEntry(
        2,
        datetime.now() - timedelta(days=3),
        "borrow",
        "borrow_record",
        1,
        users[1],
        "127.0.0.1",
        "Borrowed 1 Industrial Wrench.",
    ),
    AuditLogEntry(
        3,
        datetime.now() - timedelta(days=2),
        "return",
        "return_record",
        1,
        users[2],
        "127.0.0.1",
        "Returned 1 Hydraulic Pump in good condition.",
    ),
]

audit_logs = fair_audit


def get_user_by_id(user_id: int) -> Optional[User]:
    return next((user for user in users if user.id == user_id), None)


def get_spare_by_id(spare_id: int) -> Optional[Spare]:
    return next((spare for spare in spares if spare.id == spare_id), None)


def get_borrow_by_id(borrow_id: int) -> Optional[BorrowRecord]:
    return next((borrow for borrow in borrow_records if borrow.id == borrow_id), None)


@app.before_request
def load_user():
    user_id = session.get("user_id")
    g.current_user = get_user_by_id(user_id) if user_id else None
    if request.endpoint not in ("login", "static") and g.current_user is None:
        return redirect(url_for("login"))


@app.context_processor
def inject_current_user():
    return {"current_user": getattr(g, "current_user", None)}


@app.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = next(
            (u for u in users if u.username == username and u.password == password),
            None,
        )
        if user:
            session["user_id"] = user.id
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout", endpoint="auth.logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/", endpoint="main.dashboard")
def dashboard():
    stats = {
        "total_spares": len(spares),
        "low_stock": sum(
            1 for spare in spares if spare.quantity_in_stock <= spare.minimum_quantity
        ),
        "active_borrows": sum(1 for borrow in borrow_records if not borrow.is_returned),
    }
    return render_template("dashboard.html", stats=stats)


@app.route("/spares", endpoint="spares.list_spares")
def list_spares():
    page = int(request.args.get("page", 1))
    search = request.args.get("search", "").strip()
    filter_type = request.args.get("type", "").strip()
    filtered = [
        spare
        for spare in spares
        if (
            not search
            or search.lower() in spare.name.lower()
            or search.lower() in (spare.part_number or "").lower()
        )
        and (not filter_type or spare.item_type == filter_type)
    ]
    pagination = Pagination(filtered, page)
    return render_template(
        "spares/list.html", spares=pagination, search=search, filter_type=filter_type
    )


@app.route("/spares/add", methods=["GET", "POST"], endpoint="spares.add_spare")
def add_spare():
    if request.method == "POST":
        new_id = max((spare.id for spare in spares), default=0) + 1
        item_type = request.form.get("item_type", "").strip() or "consumable"
        spares.append(
            Spare(
                new_id,
                request.form.get("name", "New Spare").strip() or "New Spare",
                request.form.get("description", "").strip(),
                request.form.get("part_number", "").strip() or None,
                item_type,
                max(0, int(request.form.get("quantity_in_stock", 0))),
                max(1, int(request.form.get("minimum_quantity", 1))),
                request.form.get("unit", "").strip() or "pcs",
                request.form.get("location", "").strip() or None,
            )
        )
        flash("Spare created successfully.", "success")
        return redirect(url_for("spares.list_spares"))
    return render_template("spares/add.html")


@app.route(
    "/spares/<int:spare_id>/edit", methods=["GET", "POST"], endpoint="spares.edit_spare"
)
def edit_spare(spare_id: int):
    spare = get_spare_by_id(spare_id)
    if spare is None:
        flash("Spare not found.", "error")
        return redirect(url_for("spares.list_spares"))
    if request.method == "POST":
        spare.name = request.form.get("name", spare.name).strip() or spare.name
        spare.description = (
            request.form.get("description", spare.description).strip()
            or spare.description
        )
        spare.part_number = (
            request.form.get("part_number", spare.part_number).strip()
            or spare.part_number
        )
        spare.item_type = (
            request.form.get("item_type", spare.item_type).strip() or spare.item_type
        )
        spare.quantity_in_stock = max(
            0, int(request.form.get("quantity_in_stock", spare.quantity_in_stock))
        )
        spare.minimum_quantity = max(
            1, int(request.form.get("minimum_quantity", spare.minimum_quantity))
        )
        spare.unit = request.form.get("unit", spare.unit).strip() or spare.unit
        spare.location = (
            request.form.get("location", spare.location).strip() or spare.location
        )
        flash("Spare updated successfully.", "success")
        return redirect(url_for("spares.list_spares"))
    return render_template("spares/edit.html", spare=spare)


@app.route(
    "/spares/<int:spare_id>/delete", methods=["POST"], endpoint="spares.delete_spare"
)
def delete_spare(spare_id: int):
    spare = get_spare_by_id(spare_id)
    if spare is not None:
        spares.remove(spare)
        flash("Spare deleted.", "success")
    else:
        flash("Spare not found.", "error")
    return redirect(url_for("spares.list_spares"))


@app.route("/borrows", endpoint="borrow.list_borrows")
def list_borrows():
    page = int(request.args.get("page", 1))
    status = request.args.get("status", "").strip()
    filtered = [
        borrow
        for borrow in borrow_records
        if (status == "returned" and borrow.is_returned)
        or (status == "active" and not borrow.is_returned)
        or not status
    ]
    pagination = Pagination(filtered, page)
    return render_template("borrow/list.html", borrows=pagination, status=status)


@app.route("/borrow", methods=["GET", "POST"], endpoint="borrow.borrow_item")
def borrow_item():
    available = [spare for spare in spares if spare.quantity_in_stock > 0]
    if request.method == "POST":
        spare_id = int(request.form.get("spare_id", 0))
        quantity = max(1, int(request.form.get("quantity", 1)))
        spare = get_spare_by_id(spare_id)
        if spare is None:
            flash("Selected spare not found.", "error")
        elif quantity > spare.quantity_in_stock:
            flash("Quantity exceeds available stock.", "error")
        else:
            spare.quantity_in_stock -= quantity
            new_id = max((borrow.id for borrow in borrow_records), default=0) + 1
            borrow_records.append(
                BorrowRecord(
                    new_id,
                    spare,
                    quantity,
                    g.current_user,
                    datetime.now(),
                    None,
                    False,
                )
            )
            flash("Borrow record created.", "success")
            return redirect(url_for("borrow.list_borrows"))
    return render_template("borrow/borrow.html", spares=available)


@app.route("/returns", endpoint="return.list_returns")
def list_returns():
    page = int(request.args.get("page", 1))
    pagination = Pagination(return_records, page)
    return render_template("return/list.html", returns=pagination)


@app.route("/return", methods=["GET", "POST"], endpoint="return.return_item")
def return_item():
    active_borrows = [borrow for borrow in borrow_records if not borrow.is_returned]
    if request.method == "POST":
        borrow_id = int(request.form.get("borrow_id", 0))
        quantity_returned = max(1, int(request.form.get("quantity_returned", 1)))
        condition = request.form.get("condition", "").strip() or None
        notes = request.form.get("notes", "").strip() or None
        borrow = get_borrow_by_id(borrow_id)
        if borrow is None:
            flash("Borrow record not found.", "error")
        else:
            return_record = ReturnRecord(
                max((record.id for record in return_records), default=0) + 1,
                borrow,
                quantity_returned,
                condition,
                g.current_user,
                datetime.now(),
                notes,
            )
            return_records.append(return_record)
            borrow.spare.quantity_in_stock += quantity_returned
            if quantity_returned >= borrow.quantity:
                borrow.is_returned = True
            flash("Return recorded.", "success")
            return redirect(url_for("return.list_returns"))
    return render_template("return/return.html", borrows=active_borrows)


@app.route("/reports/audit-log", endpoint="reports.audit_log_view")
def audit_log_view():
    page = int(request.args.get("page", 1))
    entity_type = request.args.get("entity_type", "").strip()
    filtered = [
        entry
        for entry in audit_logs
        if not entity_type or entry.entity_type == entity_type
    ]
    logs = Pagination(filtered, page)
    return render_template("reports/audit_log.html", logs=logs, entity_type=entity_type)


@app.route("/reports/inventory", endpoint="reports.inventory_report")
def inventory_report():
    low_stock = [
        spare for spare in spares if spare.quantity_in_stock <= spare.minimum_quantity
    ]
    return render_template("reports/inventory.html", spares=spares, low_stock=low_stock)


@app.route("/settings", endpoint="settings.settings")
def settings():
    return render_template("settings/index.html", users=users)


@app.route("/settings/users/add", methods=["POST"], endpoint="settings.add_user")
def add_user():
    new_id = max((user.id for user in users), default=0) + 1
    users.append(
        User(
            new_id,
            request.form.get("username", f"user{new_id}").strip() or f"user{new_id}",
            request.form.get("email", "").strip() or None,
            request.form.get("role", "store_manager").strip() or "store_manager",
            datetime.now(),
            True,
            request.form.get("password", "password").strip() or "password",
        )
    )
    flash("User created successfully.", "success")
    return redirect(url_for("settings.settings"))


@app.route(
    "/settings/users/<int:user_id>/toggle",
    methods=["POST"],
    endpoint="settings.toggle_user",
)
def toggle_user(user_id: int):
    user = get_user_by_id(user_id)
    if user and user.id != g.current_user.id:
        user.is_active = not user.is_active
        flash("User status updated.", "success")
    else:
        flash("Cannot update this user.", "error")
    return redirect(url_for("settings.settings"))


if __name__ == "__main__":
    app.run(debug=True)
