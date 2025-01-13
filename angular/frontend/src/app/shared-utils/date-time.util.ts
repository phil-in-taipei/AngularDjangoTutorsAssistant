import { DurationOptionsInterface } from "../models/time-related.model";

export function getClassDurationsOptions(): DurationOptionsInterface[] {
  const classDurationOptions: DurationOptionsInterface[] = [
    { stringVal: '30 mins', timeArr: [0, 30] },
    { stringVal:'45 mins', timeArr: [0, 45] },
    { stringVal:'1 hr', timeArr: [1, 0] },
    { stringVal:'1 hr 15 mins', timeArr: [1, 15] },
    { stringVal:'1 hr 30 mins', timeArr: [1, 30] },
    { stringVal: '1 hr 45 mins', timeArr: [1, 45] },
    { stringVal:'2 hrs', timeArr: [2, 0] },
    { stringVal:'2 hrs 15 mins', timeArr: [2, 15] },
    { stringVal:'2 hrs 30 mins', timeArr: [2, 30] },
    { stringVal:'2 hrs 45 mins', timeArr: [2, 45] },
    { stringVal:'3 hrs', timeArr: [3, 0] },
    { stringVal:'3 hrs 15 mins', timeArr: [3, 15] },
    { stringVal:'3 hrs 30 mins', timeArr: [3, 30] },
    { stringVal:'3 hrs 45 mins', timeArr: [3, 45] },
    { stringVal:'4 hrs', timeArr: [4, 0] },
    { stringVal:'4 hrs 15 mins', timeArr: [4, 15] },
    { stringVal:'4 hrs 30 mins', timeArr: [4, 30] },
    { stringVal:'4 hrs 45 mins', timeArr: [4, 45] },
    { stringVal:'5 hrs', timeArr: [5, 0]}
  ];
  return classDurationOptions;
}


export function getDateString(
    day: number, month: number, year: number
    ): string {
    let monthStr;
    if (month > 0 && month < 10) {
      monthStr = '0' + month.toString();
    } else {
      monthStr = month.toString();
    }
    let dayOfMonthStr;
    if (day > 0 && day < 10) {
      dayOfMonthStr = '0' + day.toString();
    } else {
      dayOfMonthStr = day.toString();
    }
    let dateString = `${year}-${monthStr}-${dayOfMonthStr}`;
    return dateString;
  }
  

  export function getFormattedTime(
    startNum: number, endNum: number
  ): string {
    let hour = startNum.toString();
    if (startNum < 10) {
      hour = `0${hour}`;
    }
    let minutes = endNum.toString();
    if (endNum < 10) {
      minutes = `0${minutes}`;
    }
    let formattedTime =  `${hour}:${minutes}`
    return formattedTime
  }

export function getFinishTime(
  startTimeDate: Date, classDuration: String[]
): string {
  let finishTimeDate = startTimeDate;
  console.log(classDuration)
  finishTimeDate.setHours(
    finishTimeDate.getHours() + +classDuration[0]);
  finishTimeDate.setMinutes(
    finishTimeDate.getMinutes() + +classDuration[1] - 1);
  // 1 minute subtracted to avoid scheduling overlap conflict
  // add 1 minute on when calculating hours in student account
  console.log(finishTimeDate)
  return getFormattedTime(
    finishTimeDate.getHours(), finishTimeDate.getMinutes()
  )
}  
  
export function getFirstDateofMonthStr(month: number, year: number): string {
    let dateStr: string;
    if (month < 10) {
      dateStr = `${year}-0${month}-01`;
    } else {
      dateStr = `${year}-${month}-01`;
    }
    return dateStr
  }
  
  export function getFirstDateofNextMonthStr(month: number, year: number):string {
    let dateStr: string;
    let newMonth: number;
    let newYear: number;
    if (month == 12) {
      newMonth = 1
      newYear = year + 1
    } else {
      newMonth = month + 1
      newYear = year
    }
    if (newMonth < 10) {
      dateStr = `${newYear}-0${newMonth}-01`;
    } else {
      dateStr = `${newYear}-${newMonth}-01`;
    }
    return dateStr
  }
  
  export function getLastDateOfMonthStr(month: number, year: number):string {
    let date = new Date();
    date.setFullYear(year);
    date.setMonth(month);
    date.setDate(1);
    date.setDate(date.getDate() -1);
    return getDateString(
      date.getUTCDate(),
      date.getUTCMonth() + 1,
      date.getUTCFullYear()
    );
  }
  
  export function getSecondDateofMonthStr(month: number, year: number):string {
    let dateStr: string;
    if (month < 10) {
      dateStr = `${year}-0${month}-02`;
    } else {
      dateStr = `${year}-${month}-02`;
    }
    return dateStr
  }
  
  export function getYearsOptions(): number[] {
    let nextYear = new Date().getFullYear() + 2;
    const firstYear = 2024;
    let years = []
    for (let i = firstYear; i < nextYear; i++) {
      console.log(i)
      years.push(i)
    }
    return years;
  }
  
  export const monthsAndIntegers: [string, number][] = [
    ['January', 1],
    ['February', 2],
    ['March', 3],
    ['April', 4],
    ['May', 5],
    ['June', 6],
    ['July', 7],
    ['August', 8],
    ['September', 9],
    ['October', 10],
    ['November', 11],
    ['December', 12]
  ];
  