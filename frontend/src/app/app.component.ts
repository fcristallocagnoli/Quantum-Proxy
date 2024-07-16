import { Component, HostListener, OnInit } from '@angular/core';

import { AccountService } from './_services';
import { Account, Role } from './_models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  Role = Role;
  account?: Account | null;

  showScroll: boolean = false;

  themes = ['light', 'dark', 'auto'];
  activeTheme: string;

  constructor(private accountService: AccountService) {
    this.accountService.account.subscribe(x => this.account = x);
    this.activeTheme = this.getPreferredTheme();
  }

  ngOnInit(): void {
    this.setTheme(this.activeTheme);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      const storedTheme = this.getStoredTheme();
      if (storedTheme !== 'light' && storedTheme !== 'dark') {
        this.setTheme(this.getPreferredTheme());
      }
    });
  }

  logout() {
    this.accountService.logout();
    // para solucionar un pequeño bug. el dropdown no se cierra al hacer logout
    document.getElementById('logout-user')?.click();
  }

  @HostListener('window:scroll', [])
  onWindowScroll(): void {
    const scrollPosition = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop;
    this.showScroll = scrollPosition > 300;
  }

  scrollToTop(): void {
    window.scroll({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  }

  // Theme functions

  getStoredTheme(): string | null {
    return localStorage.getItem('theme');
  }

  setStoredTheme(theme: string): void {
    localStorage.setItem('theme', theme);
  }

  getPreferredTheme(): string {
    const storedTheme = this.getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  setTheme(theme: string): void {
    if (theme === 'auto') {
      document.documentElement.setAttribute('data-bs-theme', window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme);
    }
  }

}