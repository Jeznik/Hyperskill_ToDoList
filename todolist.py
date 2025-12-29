from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today)

    def __repr__(self):
        return f"Task(id={self.id}, task='{self.task}', deadline={self.deadline})"


class TodoListApp:
    def __init__(self):
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def run(self):
        while True:
            menu = ["1) Today's tasks", "2) Add a task", "0) Exit"]
            for option in menu:
                print(option)

            user_input = input()

            if user_input not in ["0", "1", "2"]:
                print("Invalid input. Please try again.")
                continue
            elif user_input == "0":
                print("Bye!")
                break
            elif user_input == "1":
                self.get_todays_tasks()
            elif user_input == "2":
                self.add_task()

    def get_todays_tasks(self):
        rows = self.session.query(Task).all()
        if not rows:
            print("Nothing to do!")
        else:
            for row in rows:
                print(row)

    def add_task(self):
        new_task = input("Enter a task\n")
        self.session.add(Task(task=new_task))
        self.session.commit()
        print("The task has been added!")


def main():
    app = TodoListApp()
    app.run()

if __name__ == "__main__":
    main()
