from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError

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
            menu = ["1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Missed tasks",
                    "5) Add a task ", "6) Delete a task ", "0) Exit"]
            for option in menu:
                print(option)

            user_input = input()

            if user_input not in ["0", "1", "2", "3", "4", "5", "6"]:
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
                self.get_missed_tasks()
            elif user_input == "5":
                print()
                self.add_task()
            elif user_input == "6":
                print()
                self.delete_task()

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
        self.print_rows(rows, "Nothing to do!")

    def print_rows(self, rows, not_rows_message):
        if not rows:
            print(not_rows_message)
        else:
            for row in rows:
                print(f"{row.id}. {row.task}. {row.deadline.strftime('%#d %b')}")

    def get_all_tasks(self):
        print("All tasks:")
        rows = self.session.query(Task).order_by(Task.deadline).all()
        self.print_rows(rows, "Nothing to do!")
        print()

    def get_missed_tasks(self):
        print("Missed tasks:")
        today = datetime.today().date()
        rows = self.session.query(Task).filter(Task.deadline < today).all()
        self.print_rows(rows, "All tasks have been completed!")
        print()

    def add_task(self):
        new_task = input("Enter a task\n")
        new_deadline = datetime.strptime(input("Enter a deadline\n"), "%Y-%m-%d")
        self.session.add(Task(task=new_task, deadline=new_deadline))
        self.session.commit()
        print("The task has been added!")
        print()

    def delete_task(self):
        print("Choose the number of the task you want to delete:")
        rows = self.session.query(Task).order_by(Task.deadline).all()
        self.print_rows(rows, "Nothing to delete")
        task_id = int(input())
        task = self.session.get(Task, task_id)
        try:
            self.session.delete(task)
            self.session.commit()
            print("The task has been deleted!")
        except UnmappedInstanceError:
            print("Invalid task ID. Task not found.")
        print()


def main():
    app = TodoListApp()
    app.run()

if __name__ == "__main__":
    main()
