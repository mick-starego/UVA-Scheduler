
let courseData = [];
let classesSelected = [];

async function loadCourseData() {
    return $.get('/scheduler/data', (data) => {
        courseData = data['courses'];
    });
}


function getCourseString(c) {
    return c['Mnemonic'] + ' ' + c['Number'] + '-' + c['Section'] + ': ' + c['Title'] + ' - ' + c['Instructor(s)'];
}


function updateClassList() {
    let classListInnerHTML = '';
    classesSelected.forEach((c) => classListInnerHTML += constructLi(getCourseString(c)));
    document.getElementById('class-list').innerHTML = classListInnerHTML;
}


function getClass(mnemonic, number, section) {
    return courseData.find((c) => c['Mnemonic'] === mnemonic && c['Number'] + '' === number && c['Section'] + '' === section);
}


function addClass() {
    document.getElementById('placeholder').style.display = 'none';
    document.getElementById('gen-btn').disabled = false;
    const uvaClass = getClass(document.getElementById('mnemonic-select').value,
                              document.getElementById('course-select').value,
                              document.getElementById('section-select').value);
    if (uvaClass != null && classesSelected.find(
            (c) => c['Mnemonic'] === uvaClass['Mnemonic'] &&
                   c['Number'] === uvaClass['Number'] &&
                   c['Section'] === uvaClass['Section']) == null) {
        classesSelected.unshift(uvaClass);
        updateClassList();
    }
}


function removeClass(courseString) {
    classesSelected = classesSelected.filter((c) => getCourseString(c) !== courseString);
    if (classesSelected.length === 0) {
        document.getElementById('placeholder').style.display = 'flex';
        document.getElementById('gen-btn').disabled = true;
    }
    updateClassList();
}


function updateSelects(mnemonicChanged) {
    const mnemonicSelected = document.getElementById('mnemonic-select').value;
    let courseSelected = document.getElementById('course-select').value;

    if (!courseSelected || mnemonicChanged) {
        let courseNumInnerHTML = '';
        deDupe(courseData.filter((c) => c['Mnemonic'] === mnemonicSelected), (c) => c['Number'])
            .forEach((c) => courseNumInnerHTML += constructOption(c['Number'], c['Number'] + ' - ' + c['Title']));
        document.getElementById('course-select').innerHTML = courseNumInnerHTML;
    }

    courseSelected = document.getElementById('course-select').value;
    let sectionInnerHTML = '';
    deDupe(courseData.filter((c) => c['Mnemonic'] === mnemonicSelected && c['Number'] + '' === courseSelected), (c) => c['Section'])
        .forEach((c) => sectionInnerHTML += constructOption(c['Section'], c['Section'] + ' - ' + c['Instructor(s)']));
    document.getElementById('section-select').innerHTML = sectionInnerHTML;
}


function constructOption(v, s) {
    return '<option value="' + v + '">' + s + '</option>';
}


function constructLi(s) {
    return '<li class="list-group-item"><span class="inner-li">' + s + '<i class="fas fa-trash trash-icon" onclick="removeClass(\'' + s + '\')\"></i></span></li>';
}


function deDupe(collection, key=(x)=>x) {
    const set = new Set();
    const result = [];
    collection.forEach((x) => {
        if (!set.has(key(x))) {
            result.push(x);
            set.add(key(x));
        }
    });
    return result.sort((a,b)=>a < b ? -1 : 1);
}


window.addEventListener('load', async function() {
    loadCourseData().then(() => {
        let mnemonicInnerHTML = '';
        deDupe(courseData.map((c) => c['Mnemonic']))
            .forEach((m) => mnemonicInnerHTML += constructOption(m, m));
        document.getElementById('mnemonic-select').innerHTML = mnemonicInnerHTML;

        updateSelects();
    });

    // TODO remove
    loadSchedule(mockSchedules[0]);
});


// ****************************** Schedule ******************************

const mockSchedules = [
    [
        {
            name: 'CS 2150-002',
            days: 'Tu 6:00pm - 6:50pm'
        },
        {
            name: 'CS 3330-001',
            days: 'MoWeFr 10:00am - 10:50am'
        },
        {
            name: 'APMA 3100-003',
            days: 'TuTh 9:30am - 10:45am'
        },
        {
            name: 'MSE 2090-001',
            days: 'Fr 9:00am - 9:50am'
        },
        {
            name: 'STS 1500-010',
            days: 'Th 1:00pm - 1:50pm'
        }
    ],
    [
        {
            name: 'CS 4620-001',
            days: 'TuTh 11:00am - 12:15pm'
        },
        {
            name: 'CS 4710-001',
            days: 'TuTh 5:00pm - 6:15pm'
        },
        {
            name: 'STS 4500-007',
            days: 'MoWe 3:00pm - 4:45pm'
        },
        {
            name: 'CS 4414-001',
            days: 'MoWe 5:00pm - 6:15pm'
        }
    ],
    [
        {
            name: 'CS 2110-002',
            days: 'MoWeFr 10:00am - 10:50am'
        }
    ],
    [
        {
            name: 'CS 2150-001',
            days: 'MoWe 1:00pm - 2:15pm'
        }
    ]
];

let currentColorIndex = 0;
let maxColorIndex = 4;

let currentScheduleIndex = 0;


function loadNextSchedule() {
    if (currentScheduleIndex === mockSchedules.length - 1) {
        currentScheduleIndex = 0;
    } else {
        currentScheduleIndex++;
    }
    loadSchedule(mockSchedules[currentScheduleIndex]);
}


function loadPreviousSchedule() {
    if (currentScheduleIndex === 0) {
        currentScheduleIndex = mockSchedules.length - 1;
    } else {
        currentScheduleIndex--;
    }
    loadSchedule(mockSchedules[currentScheduleIndex]);
}


function loadSchedule(s) {
    currentColorIndex = 0;
    const days = {
        'MO': [],
        'TU': [],
        'WE': [],
        'TH': [],
        'FR': []
    }
    s.forEach((c) => {
        buildAllClassBlocks(c).forEach((b) => {
            console.log(b);
            let [k, blockHTML] = b;
            days[k].push(blockHTML);
        });
    });
    Object.keys(days).forEach((k) => {
         let innerHTML = '';
         days[k].forEach((s) => innerHTML += s);
         document.getElementById(k).innerHTML = innerHTML;
    });
}



function parseTime(s) {
    let [hrs, mins] = s.slice(0, s.length - 2).split(':');
    if (s.substring(s.length - 2, s.length).toUpperCase() === 'AM' || hrs === '12') {
        return (parseInt(hrs) - 8) * 60 + parseInt(mins);
    } else {
        return ((4 + parseInt(hrs)) * 60) + parseInt(mins);
    }
}


/**
 * @param s string
 * @returns {{dayStr, start: *, end: *}}
 */
function parseDayTime(s) {
    let [dayStr, start, _, end] = s.split(' ');
    return [dayStr.toUpperCase(), (start + ' - ' + end), parseTime(start), parseTime(end)];
}


function buildSingleClassBlock(name, timeStr, start, end, colorIndex) {
    const top = (start + 17) + 'px';
    const height = (end - start) + 'px';
    return '<div class="class-block color-' + colorIndex + '" style="top: ' + top + '; height: ' + height + ';">' +
        '<span class="class-name">' + name + '</span>' +
        '<span class="class-time">' + timeStr + '</span>' +
        '</div>';
}


function buildAllClassBlocks(c) {
    let [dayStr, timeStr, start, end] = parseDayTime(c.days);
    const colorIndex = getNextColorIndex();
    const result = [];

    if (dayStr.includes('MO')) {
        result.push(['MO', buildSingleClassBlock(c.name, timeStr, start, end, colorIndex)]);
    }
    if (dayStr.includes('TU')) {
        result.push(['TU', buildSingleClassBlock(c.name, timeStr, start, end, colorIndex)]);
    }
    if (dayStr.includes('WE')) {
        result.push(['WE', buildSingleClassBlock(c.name, timeStr, start, end, colorIndex)]);
    }
    if (dayStr.includes('TH')) {
        result.push(['TH', buildSingleClassBlock(c.name, timeStr, start, end, colorIndex)]);
    }
    if (dayStr.includes('FR')) {
        result.push(['FR', buildSingleClassBlock(c.name, timeStr, start, end, colorIndex)]);
    }
    return result;
}


function getNextColorIndex() {
    if (currentColorIndex === maxColorIndex) {
        currentColorIndex = 0;
    } else {
        currentColorIndex++;
    }
    return currentColorIndex;
}