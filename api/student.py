from flask import Blueprint, jsonify, request

from database import db
from models.pydantic.students.student_read import StudentReadModel
from models.pydantic.students.student_update import StudentUpdateModel
from models.sqlalchemy.student import Student

students_bp = Blueprint("students_bp", __name__, url_prefix="/students")


@students_bp.route("/", methods=["GET"])
def get_all_students():
    students = Student.query.all()
    print(students)
    return jsonify({"students": [StudentReadModel.model_validate(s).model_dump(mode="json") for s in students]})


@students_bp.route("/<int:pk>", methods=["GET"])
def get_student_by_id(pk):
    student = Student.query.get(pk)
    if student is None:
        return jsonify({"error": f"Student with id={pk} not found"}), 404

    return jsonify(StudentReadModel.model_validate(student).model_dump(mode="json"))


@students_bp.route("/search", methods=["GET"])
def search_students():
    name_query = request.args.get("name", "")
    students = Student.query.filter(Student.name.ilike(f"%{name_query}%")).all()
    return jsonify({"students": [StudentReadModel.model_validate(s).model_dump(mode="json") for s in students]})


@students_bp.route("/<int:pk>", methods=["DELETE"])
def delete_student_by_id(pk):
    student = Student.query.get(pk)
    if student is None:
        return jsonify({"error": f"Student with id={pk} not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student was successfully deleted"}), 204


@students_bp.route("/<int:pk>", methods=["PATCH"])
def edit_student_by_id(pk):
    student = Student.query.get(pk)
    if student is None:
        return jsonify({"error": f"Student with id={pk} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": f"No data provided"}), 400

    validated_data = StudentUpdateModel.model_validate(data)
    for field, value in validated_data.model_dump(exclude_none=True).items():
        if value is not None:
            setattr(student, field, value)  # Updates all fields, including course_name and photo_url
    db.session.commit()

    return jsonify(StudentReadModel.model_validate(student).model_dump(mode="json"))


@students_bp.route("/", methods=["POST"])
def create_student_by_id():

    data = request.get_json()
    if not data:
        return jsonify({"error": f"No data provided"}), 400

    validated_data = StudentUpdateModel.model_validate(data)
    new_student = Student(**validated_data.model_dump())

    db.session.add(new_student)
    db.session.commit()

    return jsonify(StudentReadModel.model_validate(new_student).model_dump(mode="json")), 201
