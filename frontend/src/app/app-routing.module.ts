import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home';
import { authGuard } from './_helpers';
import { Role } from './_models';
import { NotFoundComponent } from './_components/not-found.component';

const accountModule = () => import('./account/account.module').then(x => x.AccountModule);
const providersModule = () => import('./providers/providers.module').then(x => x.ProvidersModule);
const systemsModule = () => import('./systems/systems.module').then(x => x.SystemsModule);
const comparativeModule = () => import('./comparative/comparative.module').then(x => x.ComparativeModule);
const wizardModule = () => import('./wizard/wizard.module').then(x => x.WizardModule);
const adminModule = () => import('./admin/admin.module').then(x => x.AdminModule);
const profileModule = () => import('./profile/profile.module').then(x => x.ProfileModule);
const jobsModule = () => import('./jobs/jobs.module').then(x => x.JobsModule);

const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'providers', loadChildren: providersModule },
    { path: 'systems', loadChildren: systemsModule },
    { path: 'compare', loadChildren: comparativeModule },
    { path: 'wizard', loadChildren: wizardModule },
    { path: 'account', loadChildren: accountModule },
    { path: 'profile', loadChildren: profileModule, canActivate: [authGuard] },
    { path: 'jobs', loadChildren: jobsModule, canActivate: [authGuard] },
    { path: 'admin', loadChildren: adminModule, canActivate: [authGuard], data: { roles: [Role.Admin] } },
    { path: 'not-found', component: NotFoundComponent},

    // otherwise redirect to home
    { path: '**', redirectTo: 'not-found' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes, {scrollPositionRestoration: 'enabled'})],
    exports: [RouterModule]
})
export class AppRoutingModule { }
