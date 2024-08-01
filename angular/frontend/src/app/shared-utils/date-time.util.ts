
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
  
  
  export function getFirstDateofMonthStr(month: number, year: number):string {
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
  