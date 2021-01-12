import os
from prod_break import app, db

if __name__ == "__main__":
    if "site.db" not in os.listdir("prod_break"):
        db.create_all()
    app.run(debug=True)