import { Role } from './role';

export class Platform {
    platform: string;
    apiKeys: Map<string, string>;
}

export class Account {
    id?: string;
    firstName?: string;
    lastName?: string;
    email?: string;
    role?: Role;
    apiKeys?: Platform[];
    jwtToken?: string;
}