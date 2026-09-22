from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'future-solutions-secret-key-2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///futuresolutions.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.models import QuoteRequest

    with app.app_context():
        db.create_all()

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
                'description': 'Our ocean freight solutions offer secure, cost-effective transport for full container loads (FCL) and less than container loads (LCL). We partner with major global shipping lines to ensure reliable sailings, flexible scheduling, and competitive freight rates worldwide.'
            },
            'air-cargo': {
                'title': 'Air Cargo Logistics',
                'subtitle': 'Time-critical express air freight for high-priority shipments.',
                'image': 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80',
                'description': 'When speed is your highest priority, our air cargo logistics provide rapid, secure transport globally. We handle urgent commercial shipments, oversized cargo, and special handling requirements with guaranteed airline space allocations.'
            },
            'customs-clearance': {
                'title': 'Customs Clearance Solutions',
                'subtitle': 'Expert documentation and seamless regulatory compliance at international ports.',
                'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80',
                'description': 'Navigating international trade regulations can be complex. Our licensed customs brokers manage all documentation, tariff classifications, and port compliance to clear your freight smoothly without costly delays.'
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
            return "Quote Request Successfully Submitted & Saved in Database!"
            
        return render_template('quote.html')

    return app