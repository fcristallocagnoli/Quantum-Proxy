import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Provider } from '@app/_models';
import { environment } from '@environments/environment';

const baseUrl = `${environment.apiUrl}/providers`;

const providersProjection = {
  projection: {
    name: 1,
    description: 1,
    website: 1,
    from_third_party: 1,
    third_party: 1
  }
};


@Injectable({ providedIn: 'root' })
export class ProviderService {

  constructor(private http: HttpClient) { }

  getAll() {
    return this.http.post<Provider[]>(baseUrl, { providersProjection });
  }

  getByPid(pid: string) {
    return this.http.get<Provider>(`${baseUrl}/${pid}`);
  }
}
