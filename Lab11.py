#lab 11
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import statistics
import math



class Gradebook:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

        self.students = {}
        self.assignments = {}
        self.assign_by_id = {}
        self.stu_subs = defaultdict(list)
        self.assn_subs = defaultdict(list)

        self.load_students()
        self.load_assignments()
        self.load_submissions()

    def load_students(self):
        with open(os.path.join(self.data_dir, "students.txt")) as f:
            for line in f:
                line = line.strip()
                sid = line[:3]
                name = line[3:].strip()
                self.students[name] = sid

    def load_assignments(self):
        path = os.path.join(self.data_dir, "assignments.txt")
        lines = [x.strip() for x in open(path) if x.strip()]

        for i in range(0, len(lines), 3):
            name = lines[i]
            aid = lines[i+1]
            pts = int(lines[i+2])
            self.assignments[name] = {"id": aid, "points": pts}
            self.assign_by_id[aid] = {"name": name, "points": pts}

    def load_submissions(self):
        folder = os.path.join(self.data_dir, "submissions")
        for file in os.listdir(folder):
            if not file.endswith(".txt"):
                continue
            sid, aid, pct = open(os.path.join(folder, file)).read().strip().split("|")
            pct = int(pct)
            self.stu_subs[sid].append({"assignment_id": aid, "percent": pct})
            self.assn_subs[aid].append(pct)

    def student_grade(self, name):
        if name not in self.students:
            return None
        sid = self.students[name]
        earned = 0
        total = sum(a["points"] for a in self.assign_by_id.values())

        for sub in self.stu_subs[sid]:
            aid = sub["assignment_id"]
            pct = sub["percent"]
            pts = self.assign_by_id[aid]["points"]
            earned += (pct/100) * pts

        return round((earned / total) * 100)

    def assignment_stats(self, name):
        if name not in self.assignments:
            return None
        aid = self.assignments[name]["id"]
        scores = self.assn_subs.get(aid, [])
        if not scores:
            return False

        mn = min(scores)
        mx = max(scores)
        avg = math.floor(statistics.mean(scores))
        return mn, avg, mx

    def plot_assignment(self, name):
        if name not in self.assignments:
            return False
        aid = self.assignments[name]["id"]
        scores = self.assn_subs.get(aid, [])
        if not scores:
            return False

        plt.hist(scores, bins=[0, 25, 50, 75, 100])
        plt.title(f"{name} Score Distribution")
        plt.xlabel("Score (%)")
        plt.ylabel("Number of Students")
        plt.show()
        return True


class App:
    def __init__(self):
        self.grade_book = Gradebook()

    def print_menu(self):
        print("1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")

        selection = input("Enter your selection: ")

        if selection == "1":
            name = input("What is the student's name: ")
            grade = self.grade_book.student_grade(name)
            if grade is None:
                print("Student not found")
            else:
                print(f"{grade}%")

        elif selection == "2":
            name = input("What is the assignment name: ")
            stats = self.grade_book.assignment_stats(name)
            if stats is None:
                print("Assignment not found")
            else:
                mn, avg, mx = stats
                print(f"Min: {mn}%")
                print(f"Avg: {avg}%")
                print(f"Max: {mx}%")

        elif selection == "3":
            name = input("What is the assignment name: ")
            if not self.grade_book.plot_assignment(name):
                print("Assignment not found")


if __name__ == "__main__":
    App().print_menu()
