import Courses
from bs4 import BeautifulSoup
from itertools import combinations
from operator import itemgetter, attrgetter


# link = 'http://sis.rutgers.edu/soc/#courses?subject=198&semester=92019&campus=NB&level=U'
# page = requests.get(link)
# soup = BeautifulSoup(page.content, 'html.parser')
def addCoursesFromFile(fname, coursesDict):
    f = open(fname, 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    for course in soup.find_all('div', {'class': 'subject'}):
        courseId = course.find('span', {'id': 'courseId'})
        if courseId is not None and courseId.text.strip() != '':
            courseId = courseId.text.strip()
        courseName = course.find('span', {'class': 'courseTitle'})
        if courseName is not None and courseName.text.strip() != '':
            courseName = courseName.text.strip()
        courseCredit = course.find('span', {'class': 'courseCredits'})
        if courseCredit is not None and courseCredit.text.strip() != '':
            courseCredit = courseCredit.text.strip()
        sections = []
        for courseSection in course.find_all('div', {'class': 'sectionData'}):
            sectionIndexNum = courseSection.find('span', {'class': 'sectionIndexNumber'})
            if sectionIndexNum is not None and sectionIndexNum.text.strip() != '':
                sectionId = sectionIndexNum.text.strip()
            days = []
            hrs = []
            for meetDay in courseSection.find_all('span', {'class': 'meetingTimeDay'}):
                if meetDay is not None and meetDay.text.strip() != '':
                    days.append(meetDay.text.strip())
            for meetHr in courseSection.find_all('span', {'class': 'meetingTimeHours'}):
                if meetHr is not None and meetHr.text.strip() != '':
                    hrs.append(meetHr.text.strip())
            i = 0
            schedules = []
            while i < len(days):
                aSchedule = Courses.schedule(days[i], hrs[i])
                schedules.append(aSchedule)
                i += 1
            section = Courses.courseSection(courseId, sectionId, schedules)
            sections.append(section)
        aCourse = Courses.course(courseId, courseName, courseCredit, sections)
        coursesDict[aCourse.courseId] = aCourse


def generateCourseSectionsCombo(myCourses, coursesOffered):
    result = []
    myWorkingArray = []
    for myCourse in myCourses:
        myCourseSections = coursesOffered[myCourse].sections
        # each of the myWorkingArray element will represent a couse I am taking
        # each element will have the sections of that couse as first element
        # size of the sections as second element
        # a counter (for generate permutation) which is set to 0 as the 3rd element
        myWorkingArray.append([myCourseSections, len(myCourseSections), 0])
    done = False
    while not done:
        oneCombo = []
        for myWorkingArrayElement in myWorkingArray:
            oneCombo.append(myWorkingArrayElement[0][myWorkingArrayElement[2]])
        result.append(oneCombo)

        r = len(myWorkingArray) - 1  # r point at the last element of myWorkingArray
        change = True
        while change and r >= 0:
            myWorkingArray[r][2] += 1  # increase the last taken couse's section's counter
            # increment the innermost variable and check if spill overs
            if myWorkingArray[r][2] >= myWorkingArray[r][1]:
                if r == 0:
                    #the outer most loop counter reaches max, we are done
                    done = True
                myWorkingArray[r][2] = 0;  # reintialize loop variable
                # Change the upper variable by one
                # We need to increment the immediate upper level loop by one
                change = True;
            else:
                change = False;  # Stop as there the upper levels of the loop are unaffected
                # We can perform any inner loop calculation here arrs[r]
            r -= 1;  # move to upper level of the loop

    return result

def generateCourseSectionsCombo1(myCourses, coursesOffered):
    results = []
    sections = []
    for myCourse in myCourses:
        sections.extend(coursesOffered[myCourse].sections)
    allCombos = combinations(sections,len(myCourses))
    for combo in allCombos:
        #my sections knows which couse they belong to
        if len(set([section.courseId for section in combo])) == len(myCourses):
            results.append(combo)
    return results


# main

courses = {}
for fname in ['cs1.txt','math1.txt','ee1.txt']:
    addCoursesFromFile(fname, courses)

#combos = generateCourseSectionsCombo(['01:198:112', '01:198:205','01:640:250','14:332:221'], courses)
combos = generateCourseSectionsCombo1(['01:198:112', '01:198:205','01:640:250','14:332:221'], courses)

goodCal = []
for combo in combos:
    s = Courses.scheduler()
    ok = True
    for aClassSection in combo:
        if not s.putCouseSectionOnGridSuccessful(aClassSection):
            ok = False
            break
    if ok:
        s.dailyHrs()
        s.freeTimeBlock()
        goodCal.append(s)
sorted(goodCal,key=attrgetter('freeTimeBlock0','freeTimeBlock1','freeTimeBlock2','freeTimeBlock3','freeTimeBlock4','freeTimeBlock5'), reverse=True)
goodCal
