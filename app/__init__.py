import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'future-solutions-secret-key-2026'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../futuresolutions.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.models import QuoteRequest, ShipmentTracking, AdminUser

    with app.app_context():
        db.create_all()
        if not AdminUser.query.filter_by(username='admin').first():
            default_admin = AdminUser(username='admin', password='future2026')
            db.session.add(default_admin)
            db.session.commit()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/services')
    def services():
        return render_template('services.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/service/<service_slug>')
    def service_detail(service_slug):
        services_data = {
            'ocean-freight': {
                'title': 'Ocean Freight Services',
                'subtitle': 'Reliable FCL and LCL container shipping across global maritime lanes.',
                'image': 'https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?auto=format&fit=crop&w=1200&q=80',
                'description': 'Our ocean freight solutions offer secure, cost-effective transport for full container loads (FCL) and less than container loads (LCL).'
            },
            'air-cargo': {
                'title': 'Air Cargo Logistics',
                'subtitle': 'Time-critical express air freight for high-priority shipments.',
                'image': 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80',
                'description': 'When speed is your highest priority, our air cargo logistics provide rapid, secure transport globally.'
            },
            'customs-clearance': {
                'title': 'Customs Clearance Solutions',
                'subtitle': 'Expert documentation and seamless regulatory compliance at international ports.',
                'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80',
                'description': 'Navigating international trade regulations can be complex with licensed customs brokers.'
            }
        }
        service = services_data.get(service_slug, services_data['ocean-freight'])
        return render_template('service_detail.html', service=service)

    @app.route('/quote', methods=['GET', 'POST'])
    def quote():
        if request.method == 'POST':
            new_quote = QuoteRequest(
                full_name=request.form.get('full_name'),
                email=request.form.get('email'),
                service_type=request.form.get('service_type'),
                incoterms=request.form.get('incoterms'),
                pickup=request.form.get('pickup'),
                destination=request.form.get('destination'),
                weight=float(request.form.get('weight') or 0),
                volume=float(request.form.get('volume') or 0),
                description=request.form.get('description')
            )
            db.session.add(new_quote)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('quote.html')

    @app.route('/admin-login', methods=['GET', 'POST'])
    def admin_login():
        error = None
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            admin = AdminUser.query.filter_by(username=username, password=password).first()
            if admin:
                session['admin_logged_in'] = True
                session['admin_username'] = admin.username
                return redirect(url_for('admin_dashboard'))
            else:
                error = 'Invalid Username or Password!'
        return render_template('admin_login.html', error=error)

    @app.route('/admin', methods=['GET', 'POST'])
    def admin_dashboard():
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))

        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'change_password':
                new_user = request.form.get('new_username')
                new_pass = request.form.get('new_password')
                admin = AdminUser.query.filter_by(username='admin').first() or AdminUser.query.first()
                if admin:
                    admin.username = new_user
                    admin.password = new_pass
                    db.session.commit()
                return redirect(url_for('admin_dashboard'))
            else:
                new_shipment = ShipmentTracking(
                    tracking_number=request.form.get('tracking_number'),
                    client_name=request.form.get('client_name'),
                    origin=request.form.get('origin'),
                    destination=request.form.get('destination'),
                    mode_of_shipment=request.form.get('mode_of_shipment'),
                    shipping_line=request.form.get('shipping_line'),
                    vessel=request.form.get('vessel'),
                    container_no=request.form.get('container_no'),
                    etd=request.form.get('etd'),
                    eta=request.form.get('eta'),
                    cargo_description=request.form.get('cargo_description'),
                    status=request.form.get('status')
                )
                db.session.add(new_shipment)
                db.session.commit()
                return redirect(url_for('admin_dashboard'))

        quotes = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).all()
        shipments = ShipmentTracking.query.order_by(ShipmentTracking.id.desc()).all()
        return render_template('admin.html', quotes=quotes, shipments=shipments)

    @app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
    def edit_shipment(id):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
            
        shipment = ShipmentTracking.query.get_or_404(id)
        
        if request.method == 'POST':
            shipment.tracking_number = request.form.get('tracking_number')
            shipment.client_name = request.form.get('client_name')
            shipment.origin = request.form.get('origin')
            shipment.destination = request.form.get('destination')
            shipment.mode_of_shipment = request.form.get('mode_of_shipment')
            shipment.shipping_line = request.form.get('shipping_line')
            shipment.vessel = request.form.get('vessel')
            shipment.container_no = request.form.get('container_no')
            shipment.etd = request.form.get('etd')
            shipment.eta = request.form.get('eta')
            shipment.cargo_description = request.form.get('cargo_description')
            shipment.status = request.form.get('status')
            
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
            
        return render_template('admin_edit.html', shipment=shipment)

    @app.route('/admin-logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        session.pop('admin_username', None)
        return redirect(url_for('admin_login'))

    from flask import jsonify # దీన్ని పైన ఇంపార్ట్ చేసుకో

    @app.route('/track', methods=['POST'])
    def track_shipment():
        tracking_num = request.form.get('tracking_number', '').strip()
        shipment = ShipmentTracking.query.filter_by(tracking_number=tracking_num).first()
        
        if not shipment:
            return jsonify({"success": False, "message": "No shipment found with this tracking number."})
            
        return jsonify({
            "success": True,
            "tracking_number": shipment.tracking_number,
            "client_name": shipment.client_name,
            "origin": shipment.origin,
            "destination": shipment.destination,
            "mode_of_shipment": shipment.mode_of_shipment or 'N/A',
            "shipping_line": shipment.shipping_line or 'N/A',
            "container_no": shipment.container_no or 'N/A',
            "vessel": shipment.vessel or 'N/A',
            "etd": shipment.etd or 'Not scheduled',
            "eta": shipment.eta or 'Not scheduled',
            "cargo_description": shipment.cargo_description or 'N/A',
            "status": shipment.status
        })

    return app