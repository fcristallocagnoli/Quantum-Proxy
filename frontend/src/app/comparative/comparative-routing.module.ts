import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ComparativeComponent } from './comparative.component';
import { CompareProvidersComponent } from './compare-providers.component';
import { CompareSystemsComponent } from './compare-systems.component';


const routes: Routes = [
    { path: '', component: ComparativeComponent },
    { path: 'providers/:versus', component: CompareProvidersComponent },
    { path: 'systems/:versus', component: CompareSystemsComponent },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ComparativeRoutingModule { }