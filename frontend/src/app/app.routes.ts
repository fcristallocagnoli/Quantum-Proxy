// Not used in this project.

import { Routes } from '@angular/router';
import { AlertComponent } from './_components/alert.component';
import { authGuard } from './_helpers/auth.guard';
import { Role } from './_models';

export const routes: Routes = [
  { path: '', component: AlertComponent, canActivate: [authGuard] },
  { path: 'account', loadChildren: () => import('./account/account.module').then(m => m.AccountModule) },
  { path: 'admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule), canActivate: [authGuard], data: { roles: [Role.Admin] } },

  // otherwise redirect to home
  { path: '**', redirectTo: '' }
];
