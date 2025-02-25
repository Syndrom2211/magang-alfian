from app import create_app, db, socketio

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    
    # Run the app with SocketIO
    socketio.run(app, debug=True, port=app.config.get('PORT', 5000))
