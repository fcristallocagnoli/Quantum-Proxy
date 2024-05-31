import { Pipe, PipeTransform } from '@angular/core';

import { Md5 } from 'ts-md5';

@Pipe({
  name: 'hash',
  standalone: true
})
export class HashPipe implements PipeTransform {

  transform(value?: string): string {
    if (!value) {
      value = 'undefined@quantum-proxy.com'
    }
    return Md5.hashStr(value);
  }

}
