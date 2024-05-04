from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

class PartModel(db.Model):
    __tablename__ = 'parts'

    sku = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    class_name = db.Column(db.String(100), nullable=False)
    date_last_updated = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'part',
        'polymorphic_on': class_name
    }

    def __repr__(self):
        return (f"Part(sku = {self.sku}, class_name = {self.class_name}, "
                f"date_last_updated = {self.date_last_updated}, quantity = {self.quantity})")


class ResistorModel(PartModel):
    __tablename__ = 'resistors'
    __mapper_args__ = {'polymorphic_identity': 'resistor'}

    def __init__(self, resistance, tolerance, sku, class_name, date_last_updated, quantity, *args, **kwargs):
        super().__init__(sku=sku, class_name=class_name, date_last_updated=date_last_updated, quantity=quantity, *args, **kwargs)
        self.resistance = resistance
        self.tolerance = tolerance

    resistance = db.Column(db.Integer, nullable=True)
    tolerance = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return (f"Resistor(sku = {self.sku}, resistance = {self.resistance}, tolerance = {self.tolerance})")


class SolderModel(PartModel):
    __tablename__ = 'solders'
    __mapper_args__ = {'polymorphic_identity': 'solder'}

    def __init__(self, solder_type, solder_length, sku, class_name, date_last_updated, quantity, *args, **kwargs):
        super().__init__(sku=sku, class_name=class_name, date_last_updated=date_last_updated, quantity=quantity, *args, **kwargs)
        self.solder_type = solder_type
        self.solder_length = solder_length

    solder_type = db.Column(db.String, nullable=True)
    solder_length = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return (f"Solder(sku = {self.sku}, solder_type = {self.solder_type}, solder_length = {self.solder_length})")


class WireModel(PartModel):
    __tablename__ = 'wires'
    __mapper_args__ = {'polymorphic_identity': 'wire'}

    def __init__(self, gauge, wire_length, sku, class_name, date_last_updated, quantity, *args, **kwargs):
        super().__init__(sku=sku, class_name=class_name, date_last_updated=date_last_updated, quantity=quantity, *args, **kwargs)
        self.gauge = gauge
        self.wire_length = wire_length

    gauge = db.Column(db.Float, nullable=True)
    wire_length = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return (f"Wire(sku = {self.sku}, gauge = {self.gauge}, wire_length = {self.wire_length})")


class DisplayCableModel(PartModel):
    __tablename__ = 'display_cables'
    __mapper_args__ = {'polymorphic_identity': 'display_cable'}

    def __init__(self, display_cable_type, display_cable_length, display_cable_color, sku, class_name, date_last_updated, quantity, *args, **kwargs):
        super().__init__(sku=sku, class_name=class_name, date_last_updated=date_last_updated, quantity=quantity, *args, **kwargs)
        self.display_cable_type = display_cable_type
        self.display_cable_length = display_cable_length
        self.display_cable_color = display_cable_color

    display_cable_type = db.Column(db.String, nullable=True)
    display_cable_length = db.Column(db.Float, nullable=True)
    display_cable_color = db.Column(db.String, nullable=True)

    def __repr__(self):
        return (f"DisplayCable(sku = {self.sku}, display_cable_type = {self.display_cable_type}, "
                f"display_cable_length = {self.display_cable_length}, display_cable_color = {self.display_cable_color})")


class EthernetCableModel(PartModel):
    __tablename__ = 'ethernet_cables'
    __mapper_args__ = {'polymorphic_identity': 'ethernet_cable'}

    def __init__(self, alpha_type, beta_type, speed, ethernet_cable_length, sku, class_name, date_last_updated, quantity, *args, **kwargs):
        super().__init__(sku=sku, class_name=class_name, date_last_updated=date_last_updated, quantity=quantity, *args, **kwargs)
        self.alpha_type = alpha_type
        self.beta_type = beta_type
        self.speed = speed
        self.ethernet_cable_length = ethernet_cable_length

    alpha_type = db.Column(db.String, nullable=True)
    beta_type = db.Column(db.String, nullable=True)
    speed = db.Column(db.String, nullable=True)
    ethernet_cable_length = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return (f"EthernetCable(sku = {self.sku}, alpha_type = {self.alpha_type}, "
                f"beta_type = {self.beta_type}, speed = {self.speed}, ethernet_cable_length = {self.ethernet_cable_length})")


part_put_args = reqparse.RequestParser()          # Parses the data that is passed in
part_put_args.add_argument("sku", type=int, help="SKU is required", required=True)

part_put_args.add_argument("class_name", type=str, help="Class name is required", required=True)
part_put_args.add_argument("quantity", type=int, help="Quantity is required", required=True)

part_put_args.add_argument("resistance", type=int, help="Invalid resistance, must be integer", required=False)
part_put_args.add_argument("tolerance", type=int, help="Invalid tolerance, must be integer", required=False)

part_put_args.add_argument("solder_type", type=str, help="Invalid solder type, must be string", required=False)
part_put_args.add_argument("solder_length", type=float, help="Invalid solder length, must be float", required=False)

part_put_args.add_argument("gauge", type=float, help="Invalid gauge, must be float", required=False)
part_put_args.add_argument("wire_length", type=float, help="Invalid wire length, must be float", required=False)

part_put_args.add_argument("display_cable_type", type=str, help="Invalid display cable type, must be string", required=False)
part_put_args.add_argument("display_cable_length", type=float, help="Invalid display cable length, must be float", required=False)
part_put_args.add_argument("display_cable_color", type=str, help="Invalid display cable color, must be string", required=False)

part_put_args.add_argument("alpha_type", type=str, help="Invalid alpha type, must be string", required=False)
part_put_args.add_argument("beta_type", type=str, help="Invalid beta type, must be string", required=False)
part_put_args.add_argument("speed", type=str, help="Invalid speed, must be string", required=False)
part_put_args.add_argument("ethernet_cable_length", type=float, help="Invalid ethernet cable length, must be float", required=False)



part_search_args = reqparse.RequestParser()
part_search_args.add_argument("sku", type=int, help="SKU", required=False)

part_search_args.add_argument("class_name", type=str, help="Class name is required", required=True)
part_search_args.add_argument("quantity", type=int, help="Quantity", required=False)

part_search_args.add_argument("resistance", type=int, help="Resistance", required=False)
part_search_args.add_argument("tolerance", type=int, help="Tolerance", required=False)

part_search_args.add_argument("solder_type", type=str, help="Solder Type", required=False)
part_search_args.add_argument("solder_length", type=float, help="Solder Length", required=False)

part_search_args.add_argument("gauge", type=float, help="Gauge", required=False)
part_search_args.add_argument("wire_length", type=float, help="Wire Length", required=False)

part_search_args.add_argument("display_cable_type", type=str, help="Display Cable Type", required=False)
part_search_args.add_argument("display_cable_length", type=float, help="Display Cable Length", required=False)
part_search_args.add_argument("display_cable_color", type=str, help="Display Cable Color", required=False)

part_search_args.add_argument("alpha_type", type=str, help="Alpha Type", required=False)
part_search_args.add_argument("beta_type", type=str, help="Beta Type", required=False)
part_search_args.add_argument("speed", type=str, help="Speed", required=False)
part_search_args.add_argument("ethernet_cable_length", type=float, help="Ethernet Cable Length", required=False)


part_patch_args = reqparse.RequestParser()
part_patch_args.add_argument("sku", type=int, help="SKU is required", required=True)
part_patch_args.add_argument("quantity", type=int, help="New quantity is required", required=True)



resistor_schema = {
    'sku': fields.Integer,
    'class_name': fields.String,
    'date_last_updated': fields.DateTime(dt_format='iso8601'),
    'quantity': fields.Integer,
    'resistance': fields.Integer,
    'tolerance': fields.Integer,
}

solder_schema = {
    'sku': fields.Integer,
    'class_name': fields.String,
    'date_last_updated': fields.DateTime(dt_format='iso8601'),
    'quantity': fields.Integer,
    'solder_type': fields.String,
    'solder_length': fields.Float,
}

wire_schema = {
    'sku': fields.Integer,
    'class_name': fields.String,
    'date_last_updated': fields.DateTime(dt_format='iso8601'),
    'quantity': fields.Integer,
    'gauge': fields.Float,
    'wire_length': fields.Float,
}

display_cable_schema = {
    'sku': fields.Integer,
    'class_name': fields.String,
    'date_last_updated': fields.DateTime(dt_format='iso8601'),
    'quantity': fields.Integer,
    'display_cable_type': fields.String,
    'display_cable_length': fields.Float,
    'display_cable_color': fields.String,
}

ethernet_cable_schema = {
    'sku': fields.Integer,
    'class_name': fields.String,
    'date_last_updated': fields.DateTime(dt_format='iso8601'),
    'quantity': fields.Integer,
    'alpha_type': fields.String,
    'beta_type': fields.String,
    'speed': fields.String,
    'ethernet_cable_length': fields.Float,
}


def generate_schema(subclass):                  # Generates a schema for a part based on its class
    schema = {}
    if subclass == ResistorModel:
        schema = resistor_schema
    elif subclass == SolderModel:
        schema = solder_schema
    elif subclass == WireModel:
        schema = wire_schema
    elif subclass == DisplayCableModel:
        schema = display_cable_schema
    elif subclass == EthernetCableModel:
        schema = ethernet_cable_schema

    return schema

class Add_Part(Resource):

    def put(self):                          # Adds a part
        args = part_put_args.parse_args()

        sku = args['sku']
        class_name = args['class_name']
        current_datetime = datetime.now()

        success = {"message": "Part sucessfully added"}

        valid_class_names = ['resistor', 'solder', 'wire', 'display_cable', 'ethernet_cable']

        if class_name not in valid_class_names:
            abort(400, message="Invalid class name. Valid class names are 'resistor', 'solder', 'wire', 'display_cable', and 'ethernet_cable'")

        if args['quantity'] < 0:
            abort(400, message="Quantity cannot be negative")  # Checks if quantity is negative

        subclasses = [ResistorModel, SolderModel, WireModel, DisplayCableModel, EthernetCableModel]
        for subclass in subclasses:
            result = subclass.query.filter_by(sku=sku).first()
            if result:
                abort(409, message="SKU taken")  # Checks if SKU exists in database

        if class_name == "resistor":
            if (not args['resistance']) or (not args['tolerance']):
                abort(400, message="Resistor characteristics not provided")

            result = ResistorModel.query.filter_by(resistance=args['resistance'], tolerance=args['tolerance']).first()

            if result:                       # Checks if part already exists in inventory
                abort(409, message="This resistor already exists in the inventory")

            part = ResistorModel(sku=args['sku'], class_name=args['class_name'],
                                 date_last_updated=current_datetime, quantity=args['quantity'],
                                 resistance=args['resistance'], tolerance=args['tolerance'])

            db.session.add(part)
            db.session.commit()

            return success, 201


        elif class_name == "solder":
            valid_solder_types = ['lead', 'lead-free', 'rosin-core', 'acid-core']

            if (not args['solder_type']) or (not args['solder_length']):
                abort(400, message="Solder characteristics not provided")

            result = SolderModel.query.filter_by(solder_type=args['solder_type'], solder_length=args['solder_length']).first()

            if result:
                abort(409, message="This solder already exists in the inventory")

            if args['solder_type'] not in valid_solder_types:
                abort(400, message="Invalid solder type. Valid solder types are 'lead', 'lead-free', 'rosin-core', and 'acid-core'")

            part = SolderModel(sku=args['sku'], class_name=args['class_name'],
                               date_last_updated=current_datetime, quantity=args['quantity'],
                               solder_type=args['solder_type'], solder_length=args['solder_length'])

            db.session.add(part)
            db.session.commit()

            return success, 201

        elif class_name == "wire":
            if (not args['gauge']) or (not args['wire_length']):
                abort(400, message="Wire characteristics not provided")

            result = WireModel.query.filter_by(gauge=args['gauge'], wire_length=args['wire_length']).first()

            if result:
                abort(409, message="This wire already exists in the inventory")

            part = WireModel(sku=args['sku'], class_name=args['class_name'],
                             date_last_updated=current_datetime, quantity=args['quantity'],
                             gauge=args['gauge'], wire_length=args['wire_length'])

            db.session.add(part)
            db.session.commit()

            return success, 201

        elif class_name == "display_cable":
            valid_display_cable_types = ['hdmi', 'vga', 'displayport', 'micro-hdmi']

            if (not args['display_cable_type']) or (not args['display_cable_length']) or (not args['display_cable_color']):
                abort(400, message="Display cable characteristics not provided")

            result = DisplayCableModel.query.filter_by(display_cable_type=args['display_cable_type'],
                             display_cable_length=args['display_cable_length'],
                             display_cable_color=args['display_cable_color']).first()

            if result:
                abort(409, message="This display cable already exists in the inventory")

            if args['display_cable_type'] not in valid_display_cable_types:
                abort(400,
                      message="Invalid display cable type. Valid display cable types are 'hdmi', 'vga', 'displayport', and 'micro-hdmi'")

            part = DisplayCableModel(sku=args['sku'], class_name=args['class_name'],
                             date_last_updated=current_datetime, quantity=args['quantity'],
                             display_cable_type=args['display_cable_type'],
                             display_cable_length=args['display_cable_length'],
                             display_cable_color=args['display_cable_color'])

            db.session.add(part)
            db.session.commit()

            return success, 201

        elif class_name == "ethernet_cable":
            valid_alpha_or_beta_types = ['male', 'female']
            valid_speeds = ['10mbps', '100mbps', '1gbps', '10gbps']

            if (not args['alpha_type']) or (not args['beta_type']) or (not args['speed']) or (not args['ethernet_cable_length']):
                abort(400, message="Ethernet cable characteristics not provided")

            result = EthernetCableModel.query.filter_by(alpha_type=args['alpha_type'], beta_type=args['beta_type'],
                             speed=args['speed'], ethernet_cable_length=args['ethernet_cable_length']).first()

            if result:
                abort(409, message="This ethernet cable already exists in the inventory")

            if args['alpha_type'] not in valid_alpha_or_beta_types:
                abort(400,
                      message="Invalid alpha type. Valid alpha types are 'male' and 'female'")

            if args['beta_type'] not in valid_alpha_or_beta_types:
                abort(400,
                      message="Invalid beta type. Valid beta types are 'male' and 'female'")

            if args['speed'] not in valid_speeds:
                abort(400,
                      message="Invalid speed. Valid speeds are '10mbps', '100mbps', '1gbps', and '10gbps'")

            part = EthernetCableModel(sku=args['sku'], class_name=args['class_name'],
                             date_last_updated=current_datetime, quantity=args['quantity'],
                             alpha_type=args['alpha_type'], beta_type=args['beta_type'],
                             speed=args['speed'], ethernet_cable_length=args['ethernet_cable_length'])

            db.session.add(part)
            db.session.commit()

            return success, 201


class Get_or_Delete_Part(Resource):

    def get(self, sku):                     # Gets a part
        # Tries to find the part in each subclass
        subclasses = [ResistorModel, SolderModel, WireModel, DisplayCableModel, EthernetCableModel]
        for subclass in subclasses:
            result = subclass.query.filter_by(sku=sku).first()
            if result:
                schema = generate_schema(subclass)
                marshaled_schema = marshal(result, schema)
                part = json.dumps(marshaled_schema, indent=4)
                return part, 200

        # If part not found in any subclass, return 404
        abort(404, message="Could not find part with that SKU")

    def delete(self, sku):              # Deletes a part
        subclasses = [ResistorModel, SolderModel, WireModel, DisplayCableModel, EthernetCableModel]
        for subclass in subclasses:
            result = subclass.query.filter_by(sku=sku).first()
            if result:
                db.session.delete(result)
                db.session.commit()
                return 204

        # If part not found in any subclass, return 404
        abort(404, message="Could not find part with that SKU")


class Quantity(Resource):

    def get(self, sku):                     # Gets the quantity of a part
        subclasses = [ResistorModel, SolderModel, WireModel, DisplayCableModel, EthernetCableModel]
        for subclass in subclasses:
            result = subclass.query.filter_by(sku=sku).first()
            if result:
                return {'sku': sku, 'quantity': result.quantity}, 200

        # If part not found in any subclass, return 404
        abort(404, message="Could not find part with that SKU")


class Inventory(Resource):

    def patch(self):                 # Adds to the inventory
        args = part_patch_args.parse_args()

        sku = args['sku']
        quantity = args['quantity']

        if quantity < 0:
            abort(400, message="Quantity cannot be negative")  # Checks if quantity given is negative

        current_datetime = datetime.now()
        subclasses = [ResistorModel, SolderModel, WireModel, DisplayCableModel, EthernetCableModel]
        for subclass in subclasses:
            result = subclass.query.filter_by(sku=sku).first()
            if result:
                result.quantity = quantity
                result.date_last_updated = current_datetime
                db.session.commit()
                success = {"message": "Quantity successfully changed"}

                return success, 200

        # If part not found in any subclass, return 404
        abort(404, message="Could not find part with that SKU")

    def get(self):                                          # Gets the inventory
        inventory_list = []
        subclasses = [ResistorModel, SolderModel, WireModel, DisplayCableModel, EthernetCableModel]
        for subclass in subclasses:
            result = subclass.query.all()
            for value in result:
                schema = generate_schema(subclass)
                marshaled_schema = marshal(value, schema)
                inventory_list.append(marshaled_schema)

        inventory = json.dumps(inventory_list, indent=4)
        return inventory, 200



class Search(Resource):

    def get(self):                          # Searches for all parts that match the provided characteristics
        search_list = []

        args = part_search_args.parse_args()

        class_name = args['class_name']

        if class_name == "resistor":

            if args['resistance'] or args['tolerance']:

                if args['resistance']:
                    result = ResistorModel.query.filter_by(resistance=args['resistance']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(ResistorModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['tolerance']:
                    result = ResistorModel.query.filter_by(tolerance=args['tolerance']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(ResistorModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

            else:
                abort(400, message="No resistor characteristics given")


        elif class_name == "solder":

            if args['solder_type'] or args['solder_length']:

                if args['solder_type']:
                    result = SolderModel.query.filter_by(solder_type=args['solder_type']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(SolderModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['solder_length']:
                    result = SolderModel.query.filter_by(solder_length=args['solder_length']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(SolderModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

            else:
                abort(400, message="No solder characteristics given")


        elif class_name == "wire":

            if args['gauge'] or args['wire_length']:

                if args['gauge']:
                    result = WireModel.query.filter_by(gauge=args['gauge']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(WireModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['wire_length']:
                    result = WireModel.query.filter_by(wire_length=args['wire_length']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(WireModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

            else:
                abort(400, message="No wire characteristics given")


        elif class_name == "display_cable":

            if args['display_cable_type'] or args['display_cable_length'] or args['display_cable_color']:

                if args['display_cable_type']:
                    result = DisplayCableModel.query.filter_by(display_cable_type=args['display_cable_type']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(DisplayCableModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['display_cable_length']:
                    result = DisplayCableModel.query.filter_by(display_cable_length=args['display_cable_length']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(DisplayCableModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['display_cable_color']:
                    result = DisplayCableModel.query.filter_by(display_cable_color=args['display_cable_color']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(DisplayCableModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

            else:
                abort(400, message="No display cable characteristics given")


        elif class_name == "ethernet_cable":

            if args['alpha_type'] or args['beta_type'] or args['speed'] or args['ethernet_cable_length']:

                if args['alpha_type']:
                    result = EthernetCableModel.query.filter_by(alpha_type=args['alpha_type']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(EthernetCableModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['beta_type']:
                    result = EthernetCableModel.query.filter_by(beta_type=args['beta_type']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(EthernetCableModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['speed']:
                    result = EthernetCableModel.query.filter_by(speed=args['speed']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(EthernetCableModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

                if args['ethernet_cable_length']:
                    result = EthernetCableModel.query.filter_by(ethernet_cable_length=args['ethernet_cable_length']).all()
                    if result:
                        for value in result:
                            schema = generate_schema(EthernetCableModel)
                            marshaled_schema = marshal(value, schema)
                            if marshaled_schema not in search_list:
                                search_list.append(marshaled_schema)

            else:
                abort(400, message="No ethernet cable characteristics given")

        search = json.dumps(search_list, indent=4)

        if len(search_list) == 0:
            search = {"message": "No parts found"}

        return search, 200

api.add_resource(Add_Part, '/part/')            # includes the put method for add_part

api.add_resource(Get_or_Delete_Part, '/part/<int:sku>')      # includes the get and delete methods for get_part and delete_part

api.add_resource(Quantity, '/quantity/<int:sku>')      # includes the get method for get_quantity

api.add_resource(Inventory, '/inventory/')

api.add_resource(Search, '/search/')            # includes the get method for search function

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)