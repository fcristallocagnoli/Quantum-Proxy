import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ComparativeComponent } from './comparative.component';
import { CompareProvidersComponent } from './compare-providers.component';


const routes: Routes = [
    { path: '', component: ComparativeComponent },
    { path: 'providers/:versus', component: CompareProvidersComponent },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ComparativeRoutingModule { }