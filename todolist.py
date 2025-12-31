from datetime import datetime, timedelta
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
            menu = ["1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Add a task", "0) Exit"]
            for option in menu:
                print(option)

            user_input = input()

            if user_input not in ["0", "1", "2", "3", "4"]:
                print("Invalid input. Please try again.")
                continue
            elif user_input == "0":
                print()
                print("Bye!")
                break
            elif user_input == "1":
                print()
                self.get_todays_tasks()
            elif user_input == "2":
                print()
                self.get_weeks_tasks()
            elif user_input == "3":
                print()
                self.get_all_tasks()
            elif user_input == "4":
                print()
                self.add_task()

    def get_todays_tasks(self):
        deadline_date = datetime.today().date()
        print(deadline_date.strftime("Today %#d %b"))
        self.get_tasks_for_date(deadline_date)
        print()

    def get_weeks_tasks(self):
        for i in range(7):
            deadline_date = datetime.today().date() + timedelta(days=i)
            print(deadline_date.strftime("%A %#d %b"))
            self.get_tasks_for_date(deadline_date)
            print()

    def get_tasks_for_date(self, deadline_date):
        rows = self.session.query(Task).filter(Task.deadline == deadline_date).all()
        if not rows:
            print("Nothing to do!")
        else:
            for i, row in enumerate(rows, start=1):
                print(f"{i}. {row.task}")

    def get_all_tasks(self):
        print("All tasks:")
        rows = self.session.query(Task).order_by(Task.deadline).all()
        if not rows:
            print("Nothing to do!")
        else:
            for i, row in enumerate(rows, start=1):
                print(f"{i}. {row.task}. {row.deadline.strftime('%#d %b')}")
        print()

    def add_task(self):
        new_task = input("Enter a task\n")
        new_deadline = datetime.strptime(input("Enter a deadline\n"), "%Y-%m-%d")
        self.session.add(Task(task=new_task, deadline=new_deadline))
        self.session.commit()
        print("The task has been added!")
        print()


def main():
    app = TodoListApp()
    app.run()

if __name__ == "__main__":
    main()
