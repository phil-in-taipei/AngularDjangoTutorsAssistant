import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'addMinute',
  standalone: false
})
export class AddMinutePipe implements PipeTransform {
  transform(value: string | null | undefined, minutesToAdd: number = 1): string {
    if (!value) {
      return '';
    }

    const parts = value.split(':').map(Number);
    if (parts.length < 2 || parts.some(isNaN)) {
      return value; // fail gracefully if format is unexpected
    }

    const [hours, minutes, seconds = 0] = parts;

    const date = new Date();
    date.setHours(hours, minutes + minutesToAdd, seconds, 0);

    const hh = date.getHours().toString().padStart(2, '0');
    const mm = date.getMinutes().toString().padStart(2, '0');

    return `${hh}:${mm}`;
  }
}
