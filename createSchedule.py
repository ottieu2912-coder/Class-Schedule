"""
void traverse(std::array<std::array<std::string, 3>, 3>& path, Class* curr, int row, int col, std::list<Class*>& classes) {
    path.at(row).at(col) = curr->name;
    classes.remove(curr);
    for (Class* s : curr->corequisite) {
        while(path.at(row).at(col) != "") row++;
        if (std::find(classes.begin(), classes.end(), s) != classes.end()) traverse(path, s, row, col, classes);
    }
    for (Class* s : curr->future) {
        row = 0;
        col++;
        while (path.at(row).at(col) != "") row++;
        if(std::find(classes.begin(), classes.end(), s)!=classes.end()) traverse(path, s, row, col, classes);
        col--;
    }
}

int reverse(Class*& lowest, Class* curr, int& temp, int& pathLength) {
    if (curr->prequisite.empty()) {
        temp++;
        if (temp > pathLength) {
            lowest = curr;
            return temp;
        }
        else return pathLength;
    }
    temp++;
    for (Class* i : curr->prequisite) {
        int now = temp;
        pathLength = reverse(lowest, i, temp, pathLength);
        temp = now;
    }
    return pathLength;
}

std::array<std::array<std::string, 3>, 3> connectedComponent(Class* curr, std::array<std::array<std::string, 3>, 3>& schedule, std::list<Class*>& classes) {
    std::array<std::array<std::string, 3>, 3> path{};
    int temp = 0;
    int pathLength = 0;
    int col = 0;
    int row = 0;
    reverse(curr, curr, temp, pathLength);
    traverse(path, curr, row, col, classes);
    int i = 0;
    for (int c = 0; c < 3; c++) {
        int r = 0;
        if (path.at(r).at(c) == "") continue;
        std::array<std::array<std::string, 3>, 3> temp = schedule;
        while (path.at(r).at(c) != "" && r < 3) {
            int j = 0;
            while (schedule.at(j).at(i) != "" && j < 2) {
                j++; 
            }
            if (j==2&&schedule.at(j).at(i) != "") {
                schedule = temp;
                i++;
            }
            else { 
                schedule.at(j).at(i) = path.at(r).at(c);
                r++;
            }
            if (r == 3)break;
        }
        i++;
    }
    return path;
}
"""

class Course:
    
    def __init__(self, name):
        self.name = name
        self.corequisite = set()
        self.fu = set()
        self.prerequisite = set()


    def Addco(self, c):
        self.corequisite.add(c)

    def Addpre(self, c):
        self.prerequisite.add(c)

    def Addfu(self, c):
        self.fu.add(c)

def organize(courses, schedule, course, x, length, points):
    #Add the difficulty of the class to the difficulty of term in points
    points[x]+= courses[course]
    #Remove the class from the list to avoid any unnecessary repeated iteration
    courses.pop(course, None)
    schedule[x].append(course.name)
    #Every class is in the same term as its corequisite.
    for co in course.corequisite:
        if co in courses:
            organize(courses, schedule, co, x, length, points)

    for f in course.fu:
        try: error = courses[f]
        except:
            continue
        organize(courses, schedule, f, x+1, length, points)

def classSchedule(courses, schedule, course, points):
    index, i, newIndex = 0, 0, 0
    lowest = course
    pathLength, temp = 0, 0
    largest = 0

    #temp and pathLength are used to measure how long a class is from class c.
    def reverse( c, temp, check):
        nonlocal lowest
        nonlocal pathLength
        temp+=1
        if not c.prerequisite:
            if temp > pathLength:
                lowest = c
                pathLength = temp
        temp+=1
        for i in c.prerequisite:
            reverse( i, temp, True)

        temp-=1
        if(check): 
            for j in c.corequisite: reverse(j, temp, False)
    reverse(course, temp, True)
    course = lowest
    pathLength,temp = 0, 0

    #We use the pathLength this time to find the length of the sequence for the maximum index, and the variable "index" is used as the minimum index.
    def findLargest(courses, course, largest, i, check, temp):
        i+=1
        nonlocal index
        nonlocal pathLength
        temp+=1
        if courses.keys().isdisjoint(course.fu):
            if temp > pathLength:
                pathLength = temp
        if courses[course] > largest: 
            index = i
            largest = courses[course]
        for f in course.fu:
            try: error = courses[f]
            except: continue
            findLargest(courses, f, largest, i, True, temp)
        
        temp-=1
        if check: 
            for co in course.corequisite: 
                findLargest(courses, co, largest, i, False, temp)
    findLargest(courses, course, largest, i, True, temp)
    index-=1
    newIndex = index
    #Search from the minimum to the maximum index for the easiest term
    for x in range (index, index+(3-pathLength)):
        if(len(schedule[x])==3): 
            if newIndex == x: newIndex+=1
            continue
        elif(points[newIndex] > points[x]): 
            newIndex = x
    newIndex-=index

    #If the sequence's length is 3, the first class of the sequence is always in the first term for the rest to fit into the schedule.
    if pathLength == 3: newIndex = 0

    organize(courses, schedule, course, newIndex, pathLength, points)


Physics7C = Course("Classical Physics I")
Physics7D = Course("Classical Physics II")
Physics7E = Course("Classical Physics III")
Math3A = Course("Linear Algebra")
ICS31 = Course("Intro to Programming")
Math2D = Course("Multivariable Calc. I")
Math2E = Course("Multivariable Calc. II")
Writing50 = Course("Basic Writing")
Writing61 = Course("Argumentative Writing")
Physics7C.Addfu(Physics7D)
Physics7D.Addpre(Physics7C)
Physics7D.Addco(Math2D)
Math2D.Addco(Physics7D)
Physics7E.Addpre(Physics7D)
Physics7D.Addfu(Physics7E)
Math2D.Addfu(Math2E)
Math2E.Addpre(Math2D)
Writing50.Addfu(Writing61)
Writing61.Addpre(Writing50)

className = {"Classical Physics I": Physics7C, "Classical Physics II": Physics7D, "Classical Physics III": Physics7E, "Multivariable Calc. I": Math2D, "Multivariable Calc. II": Math2E, "Basic Writing": Writing50, "Argumentative Writing": Writing61, "Programming": ICS31}
courses = {Physics7C: 2, Physics7D: 3, Math2E: 3, Math2D: 2}
schedule = [[], [], []]
points = [0 ,0 ,0]
courses = dict(sorted(courses.items(), key=lambda item: item[1], reverse=True))
"""
while courses:
    course = next(iter(courses))
    classSchedule(courses, schedule, course, points)

for i in range(len(schedule)):
    print(f"Row{i}: ")
    for j in range(len(schedule[i])):
        print(f"{schedule[i][j]} ")


Goal: To create a valid balanced schedule from a list of classes(the classes are called courses to avoid confusion with class in Object Oriented Programming). 
A valid schedule is a schedule where each class is in the same quarter as its corequisite and after its prerequisite.
A balanced schedule is a schedule in which every term has similar amount of difficulty. In other words, the difference between the difficulties of the terms is minimized.(Difficulty is scaled from 1 to 3)

Approach: Before we begin, we organize the terms into a list with indices from 0 to 2, and the difficulty of these terms are tracked in a list called points.
First, we sort the list of classes from the easiest to the hardest. Then, we add each class to the term with the lowest difficulty.
Through this method, when a term is too easy compared to other terms, it would receive the hard class to get closer to the other terms.
However, we first fulfill the corequisite and the prerequisite. We can treat a class and its corequisites/prerequisite as a sequence of classes.
The difficulty of the hardest class in the sequence represents the whole sequence.
Then, we must find the minimum and maximum index for this hardest class's prerequisite to be fulfilled. For example, class C has a prequisite of one class. Therefore, its minimum index is 0 and maximum index is 2.
To do this, we use the function "findLargest" to find the index by treating the sequence of classes as a graph and doing a depth-first search on it.
To do a depth-first search throughout the whole sequence, we backtrack to the first class of the sequence with a function called "reverse".
From there, we find the term with the lowest difficulty from the minimum index to the maximum index of the hardest class.
We then backtrack to the first class of the sequence. With it, we iterate through the sequence with depth-first search to fill the schedule with classes with a function called "organize".
In each iteration, we add the class's difficulty to the difficulty of the term in points. We then remove the class from the list of classes.
We apply all of these instructions to each class of the list of classes.

Time Complexity: O(n), where n is the number of classes. We have to do depth-first search to each sequence of classes, and the worst case is when the sequence covers every class in the list.

Space Complexity: O(t), where t is the number of terms. We have to keep track of the difficulty of each term.
"""