# Write your code here
class TodoListData():
    def __init__(self):
        self.todos = {}

class TodListApp():
    def __init__(self):
        self.todo_list_data = TodoListData()

    def run(self):
        self.todo_list_data.todos["Today"] = [
            "Do yoga",
            "Make a breakfast",
            "Learn the basics of SQL",
            "Learn about ORM"
        ]
        todo_day = "Today"
        print(f"{todo_day}:")
        todo_items = self.todo_list_data.todos[todo_day]
        for i, item in enumerate(todo_items, start=1):
            print(f"{i}) {item}")

def main():
    app = TodListApp()
    app.run()

if __name__ == "__main__":
    main()
