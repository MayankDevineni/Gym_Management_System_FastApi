from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import Query

class EnrollRequest(BaseModel):
    member_name: str = Field(min_length=2)
    plan_id: int = Field(gt=0)
    phone: str = Field(min_length=10)
    start_month: str = Field(min_length=3)
    payment_mode: str = "cash"
    referral_code: str = ""


class NewPlan(BaseModel):
    name: str = Field(min_length=2)
    duration_months: int = Field(gt=0)
    price: int = Field(gt=0)
    includes_classes: bool
    includes_trainer: bool

# endpoint 0 - Home  
app = FastAPI()
@app.get("/")
def home():
    return {"message" : "Welcome to Ferox lifting club! Explore our membership plans and find the perfect fit for your fitness journey."}

plans = [
    {"id": 1, "name": "Basic", "duration_months": 1, "price": 1000, "includes_classes": False, "includes_trainer": False},
    {"id": 2, "name": "Standard", "duration_months": 3, "price": 2500, "includes_classes": True, "includes_trainer": False},
    {"id": 3, "name": "Premium", "duration_months": 6, "price": 4500, "includes_classes": True, "includes_trainer": True},
    {"id": 4, "name": "Elite", "duration_months": 12, "price": 8000, "includes_classes": True, "includes_trainer": True},
    {"id": 5, "name": "Student", "duration_months": 2, "price": 1500, "includes_classes": False, "includes_trainer": False}
]


@app.get('/plans')
def get_plans():
    prices = [plan['price'] for plan in plans]
    return {
        "plans" : plans,
         "total" : len(plans),
         "min_price" : min(prices),
         "max_price" : max(prices)
    }

@app.get("/plans/summary")
def plans_summary():
    total_plans = len(plans)

    plans_with_classes = sum(1 for plan in plans if plan["includes_classes"])
    plans_with_trainer = sum(1 for plan in plans if plan["includes_trainer"])

    cheapest = min(plans, key=lambda x: x["price"])
    expensive = max(plans, key=lambda x: x["price"])

    return {
        "total_plans": total_plans,
        "plans_with_classes": plans_with_classes,
        "plans_with_trainer": plans_with_trainer,
        "cheapest_plan": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "most_expensive_plan": {
            "name": expensive["name"],
            "price": expensive["price"]
        }
    }

@app.get('/plans/{plan_id:int}')
def get_plan(plan_id: int):
    for plan in plans:
        if plan['id'] == plan_id:
            return {
                "plan": plan,
                "message": f"Plan with id {plan_id} found"
            }

    return {"message": f"Plan with id {plan_id} not found"}



memberships = []
membership_counter = 1

@app.get('/memberships')
def get_memberships():
    return {
        "memberships": memberships,
        "total": len(memberships)
    }

@app.post("/test")
def test_enroll(data: EnrollRequest):
    return {"message": "Valid data received", "data": data}


def find_plan(plan_id):
    for plan in plans:
        if plan["id"] == plan_id:
            return plan
    return None

def calculate_membership_fee(base_price, duration, payment_mode, referral_code):
    total = base_price * duration

    duration_discount = 0
    referral_discount = 0

    # duration discount
    if duration >= 12:
        duration_discount = 0.20
        total *= 0.80
    elif duration >= 6:
        duration_discount = 0.10
        total *= 0.90

    # referral discount
    if referral_code:
        referral_discount = 0.05
        total *= 0.95

    # emi charge
    if payment_mode == "emi":
        total += 200

    return total, duration_discount, referral_discount


def filter_plans_logic(max_price=None, max_duration=None, includes_classes=None, includes_trainer=None):
    filtered = plans

    if max_price is not None:
        filtered = [plan for plan in filtered if plan["price"] <= max_price]

    if max_duration is not None:
        filtered = [plan for plan in filtered if plan["duration_months"] <= max_duration]

    if includes_classes is not None:
        filtered = [plan for plan in filtered if plan["includes_classes"] == includes_classes]

    if includes_trainer is not None:
        filtered = [plan for plan in filtered if plan["includes_trainer"] == includes_trainer]

    return filtered

@app.post('/memberships')
def create_membership(data: EnrollRequest):
    global membership_counter

    plan = find_plan(data.plan_id)
    if not plan:
        return {"message": f"Plan with id {data.plan_id} not found"}

    fee, duration_discount, referral_discount = calculate_membership_fee(
        plan["price"],
        plan["duration_months"],
        data.payment_mode,
        data.referral_code
    )

    membership = {
        "membership_id": membership_counter,
        "member_name": data.member_name,
        "plan_name": plan["name"],
        "includes_classes": plan["includes_classes"],
        "duration": plan["duration_months"],
        "monthly_cost": round(fee / plan["duration_months"], 2),
        "total_fee": fee,
        "status": "active",
        "discounts": {
            "duration_discount": f"{int(duration_discount * 100)}%",
            "referral_discount": f"{int(referral_discount * 100)}%"
        }
    }
    memberships.append(membership)
    membership_counter += 1

    return {
        "message": f"Membership created successfully for {data.member_name}",
        "membership": membership
    }

@app.get('/plans/filter')
def filter_plans(
    max_price: int = Query(None),
    max_duration: int = Query(None),
    includes_classes: bool = Query(None),
    includes_trainer: bool = Query(None)
):
    result = filter_plans_logic(
        max_price,
        max_duration,
        includes_classes,
        includes_trainer
    )
    return {
        "filtered_plans": result,
        "total": len(result)
    }

@app.post('/plans' , status_code = 201)
def create_plan(data: NewPlan):
    for plan in plans:
        if plan["name"].lower() == data.name.lower():
            return {"message": "plan already exists"}

    new_plan = {
        "id": len(plans) + 1,
        "name": data.name,
        "duration_months": data.duration_months,
        "price": data.price,
        "includes_classes": data.includes_classes,
        "includes_trainer": data.includes_trainer
    }
    plans.append(new_plan)
    return {
        "message": f"Plan {data.name} created successfully",
        "plan": new_plan
    }
        
@app.put("/plans/{plan_id}")
def update_plan(
    plan_id: int,
    price: int = Query(None),
    includes_classes: bool = Query(None),
    includes_trainer: bool = Query(None)
):
    for plan in plans:
        if plan["id"] == plan_id:

            if price is not None:
                plan["price"] = price

            if includes_classes is not None:
                plan["includes_classes"] = includes_classes

            if includes_trainer is not None:
                plan["includes_trainer"] = includes_trainer

            return {"message": "Plan updated", "plan": plan}

    return {"message": "Plan not found"}

@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int):
    for i, plan in enumerate(plans):
        if plan["id"] == plan_id:
            for m in memberships:
                if m["plan_name"] == plan["name"] and m["status"] == "active":
                    return {"message": "Cannot delete plan with active members"}

            # safe to delete
            del plans[i]
            return {"message": f"Plan with id {plan_id} deleted successfully"}

    return {"message": f"Plan with id {plan_id} not found"}

class_bookings = []
class_counter = 1


@app.post("/classes/book")
def book_class(member_name: str, class_name: str, class_date: str):
    global class_counter

    valid = False
    for m in memberships:
        if m["member_name"] == member_name and m["status"] == "active" and m["includes_classes"]:
            valid = True
            break

    if not valid:
        return {"message": "Member not eligible to book classes"}

    booking = {
        "booking_id": class_counter,
        "member_name": member_name,
        "class_name": class_name,
        "class_date": class_date
    }
    class_bookings.append(booking)
    class_counter += 1
    return {"message": "Class booked successfully", "booking": booking}

@app.get("/classes/bookings")
def get_class_bookings():
    return {
        "class_bookings": class_bookings,
        "total": len(class_bookings)
    }
    
@app.delete("/classes/cancel/{booking_id}")
def cancel_booking(booking_id: int):
    for i, booking in enumerate(class_bookings):
        if booking["booking_id"] == booking_id:
            del class_bookings[i]
            return {"message": "Booking cancelled successfully"}

    return {"message": "Booking not found"}

@app.put("/memberships/{membership_id}/freeze")
def freeze_membership(membership_id: int):
    for m in memberships:
        if m["membership_id"] == membership_id:
            m["status"] = "frozen"
            return {"message": "Membership frozen", "membership": m}

    return {"message": "Membership not found"}

@app.put("/memberships/{membership_id}/reactivate")
def reactivate_membership(membership_id: int):
    for m in memberships:
        if m["membership_id"] == membership_id:
            m["status"] = "active"
            return {"message": "Membership reactivated", "membership": m}

    return {"message": "Membership not found"}
