from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields, Namespace
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
api = Api(app, version='1.0', title='University API', description='APIs for managing university tuition fees')
jwt = JWTManager(app)

tuition_model = api.model('Tuition', {
    'tuition_total': fields.Integer(description='Total tuition amount'),
    'balance': fields.Integer(description='Remaining balance'),
})

tuition_data = {
    "student1": {"tuition_total": 5000, "balance": 7500},
    "student2": {"tuition_total": 6000, "balance": 0},
    "student3": {"tuition_total": 2000, "balance": 2000},
    "student2": {"tuition_total": 1000, "balance": 560},
}

unpaid_tuition = {
    "2024Spring": ["student1", "student3"],
    "2024Autumn": ["student2", "student4"]
}


payment_parser = api.parser()
payment_parser.add_argument('student_no', type=str, required=True, help="Student number is required")
payment_parser.add_argument('term', type=str, required=True, help="Term is required")

mobile_ns = api.namespace('Mobile', description='Mobile App related operations')
banking_ns = api.namespace('Banking', description='Banking App related operations')
admin_ns = api.namespace('Admin', description='University Admin related operations')

app.config['JWT_SECRET_KEY'] = 'your_secret_key'

auth_ns = Namespace('Authentication', description='User authentication operations')

login_parser = auth_ns.parser()
login_parser.add_argument('username', type=str, required=True, help='Username')
login_parser.add_argument('password', type=str, required=True, help='Password')

@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.doc(description='User login with username and password')
    @auth_ns.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']
        if username == 'sezai' and password == '123456789':
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401

api.add_namespace(auth_ns)

@mobile_ns.route('/query-tuition')
class MobileQueryTuition(Resource):
    @jwt_required()
    @api.doc(params={'student_no': 'Student number'})
    @api.marshal_with(tuition_model)
    def get(self):
        student_no = request.args.get('student_no')
        if student_no in tuition_data:
            return tuition_data[student_no]
        else:
            return {"error": "Student not found"}, 404

@banking_ns.route('/query-tuition')
class BankingQueryTuition(Resource):
    @jwt_required()
    @api.doc(params={'student_no': 'Student number'})
    @api.marshal_with(tuition_model)
    def get(self):
        args = payment_parser.parse_args()
        student_no = args['student_no']
        if student_no in tuition_data:
            return tuition_data[student_no]
        else:
            return {"error": "Student not found"}, 404

@banking_ns.route('/pay-tuition')
class BankingPayTuition(Resource):
    @jwt_required()
    @api.doc(parser=payment_parser)
    def post(self):
        args = payment_parser.parse_args()
        student_no = args['student_no']
        term = args['term']

        if student_no in tuition_data:
            tuition_total = tuition_data[student_no]["tuition_total"]
            balance = tuition_data[student_no]["balance"]

            if balance >= tuition_total:
                return {"payment_status": "Successful"}
            else:
                tuition_data[student_no]["balance"] = balance
                return {"payment_status": "Error", "remaining_amount": tuition_total - balance}
        else:
            return {"error": "Student not found"}, 404

@admin_ns.route('/add-tuition')
class AdminAddTuition(Resource):
    @jwt_required()
    @api.doc(parser=payment_parser)
    def post(self):
        args = payment_parser.parse_args()
        student_no = args['student_no']
        term = args['term']

        return {"transaction_status": "Tuition added successfully"}

@admin_ns.route('/unpaid-tuition-status')
class AdminUnpaidTuitionStatus(Resource):
    @jwt_required()
    @api.doc(params={'term': 'Term', 'page': 'Page number', 'per_page': 'Items per page'})
    def get(self):
        term = request.args.get('term')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        if term in unpaid_tuition:
            unpaid_students = unpaid_tuition[term]
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            paginated_students = unpaid_students[start_index:end_index]
            return {"unpaid_students": paginated_students}
        else:
            return {"message": "No unpaid tuition for this term"}, 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)