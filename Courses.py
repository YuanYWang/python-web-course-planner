class schedule():
    def __init__(self, day, time):
        self.weekday = day
        self.time = time
        [f, t] = time.split(' - ')
        [tm, ap] = f.split(' ')
        [h, m] = tm.split(':')
        h = int(h)
        m = int(m)
        if ap == 'PM':
            h += 12
        self.fromMin = h * 60 + m
        [tm, ap] = t.split(' ')
        [h, m] = tm.split(':')
        h = int(h)
        m = int(m)
        if ap == 'PM':
            h += 12
        self.toMin = h * 60 + m


class courseSection():
    def __init__(self, courseId, sectionId, schedules):
        self.courseId = courseId
        self.sectionId = sectionId
        self.schedules = schedules

    def __str__(self):
        return self.courseId + '-' + self.sectionId


class course():
    def __init__(self, id, name, credit, sections):
        self.courseId = id
        self.name = name
        self.credit = credit
        self.sections = sections


class scheduler():
    weekdayToNum = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
    numToWeekday = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}

    def __init__(self):
        self.grid = []
        self.rows = 24 * 12  # 24 hrs in 5 mins slot
        self.cols = 5  # 5 weekdays
        for r in range(self.rows):
            self.grid.append([])
            for c in range(self.cols):
                self.grid[r].append('')
        self.courseSections = []

    def putCouseSectionOnGridSuccessful(self, aSection):
        for aSchedule in aSection.schedules:
            rb = (int)(aSchedule.fromMin / 5)
            re = (int)(aSchedule.toMin / 5)
            c = scheduler.weekdayToNum[aSchedule.weekday]
            for r in range(rb, re + 1):
                if self.grid[r][c] != '':
                    return False;
                self.grid[r][c] = aSection.courseId + '-' + aSection.sectionId
            self.courseSections.append(aSection.courseId + '-' + aSection.sectionId)
        return True

    def freeTimeBlock(self):
        temp = []
        for c in range(self.cols):
            dayFree = []
            r = 0;
            rb = 0
            while r < self.rows:
                while r < self.rows and self.grid[r][c] == '':
                    r += 1;
                dayFree.append(r - rb);
                while r < self.rows and self.grid[r][c] != '':
                    r += 1
                rb = r
            temp.append(dayFree)
        results = []
        i = 0
        while i < self.cols:
            results.extend(temp[i])
            if i != self.cols - 1:
                results[-1] += temp[i + 1][0]  # add the next day's beginning free time to today's last
                temp[i + 1].pop(0)
            i += 1
        results.sort(reverse=True)
        return results

    def dailyCourseHrs(self):
        result = ''
        for c in range(self.cols):
            rb = 0
            while self.grid[rb][c] == '' and rb < 24 * 12 - 1:
                rb += 1;
            re = self.rows - 1
            if rb < 24 * 12 - 1:
                while self.grid[re][c] == '':
                    re -= 1;
                bhr = (rb * 5) // 60
                bmin = (rb * 5) % 60
                ehr = (re * 5) // 60
                emin = (re * 5) % 60
                result += scheduler.numToWeekday[c][:2] + ' ' + str(bhr) + ':' + str(bmin) + '-' + str(ehr) + ':' + str(
                    emin) + ','
        result += str(self.freeTimeBlock())
        return result

    def __str__(self):
        return self.dailyCourseHrs()

    def getGrid(self):
        rB = 24 * 12 - 1
        rE = 0
        for c in range(self.cols):
            rb = 0
            while self.grid[rb][c] == '' and rb < 24 * 12 - 1:
                rb += 1;
            re = self.rows - 1
            if rb < 24 * 12 - 1:
                while self.grid[re][c] == '':
                    re -= 1;
            if rb < 24 * 12 - 1:
                if rb < rB:
                    rB = rb
                if re > rE:
                    rE = re;
        displayGrid = []
        for r in range(rE - rB + 1):
            displayGrid.append([])
            realR = r + rB
            realM = realR * 5 % 60
            realH = realR * 5 // 60
            if realM < 10:
                tStr = str(realH) + ':0' + str(realM)
            else:
                tStr = str(realH) + ':' + str(realM)
            for c in range(self.cols + 1):

                if c == 0:
                    displayGrid[r].append(tStr)
                else:
                    displayGrid[r].append(self.grid[realR][c - 1])
        displayGridFinal = []
        displayGridFinal.append(displayGrid[0])
        for r in range(1, len(displayGrid)):
            copy = False
            for c in range(1, 6):
                if r == len(displayGrid) - 1:
                    copy = True
                    break
                if displayGrid[r][c] != displayGrid[r - 1][c]:
                    copy = True
                    break
                if displayGrid[r][c] != '' and displayGrid[r + 1][c] == '':
                    copy = True
                    break
            if copy:
                displayGridFinal.append(displayGrid[r])
        return displayGrid
