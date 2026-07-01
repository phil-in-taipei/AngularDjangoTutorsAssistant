import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'formatHours'
  // no `standalone: true` — defaults to false
})
export class FormatHoursPipe implements PipeTransform {
  transform(messages: string[]): string {
    if (!messages || !messages.length) return '';

    return messages
      .map((msg, i) => i === 0 ? msg.trim() : msg.replace('Group class hours ', '').trim())
      .join(', ');
  }
}
