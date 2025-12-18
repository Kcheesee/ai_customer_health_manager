import { Link, Outlet, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LayoutDashboard, Users, FileText, Activity, Settings, LogOut } from "lucide-react";
import { NotificationBell } from "./NotificationBell";

export function MainLayout() {
    const location = useLocation();

    const navItems = [
        { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
        { href: "/accounts", label: "Accounts", icon: Users },
        { href: "/contracts", label: "Contracts", icon: FileText },
        { href: "/inputs", label: "Inputs", icon: Activity },
        { href: "/settings", label: "Settings", icon: Settings },
    ];

    return (
        <div className="flex h-screen bg-background">
            {/* Sidebar */}
            <div className="w-64 border-r flex flex-col">
                <div className="p-6">
                    <h1 className="text-xl font-bold tracking-tight flex items-center gap-2">
                        <Activity className="h-6 w-6 text-primary" />
                        Customer Pulse
                    </h1>
                </div>
                <nav className="flex-1 px-4 space-y-1">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        return (
                            <Link key={item.href} to={item.href}>
                                <Button
                                    variant={location.pathname.startsWith(item.href) ? "secondary" : "ghost"}
                                    className={cn("w-full justify-start", location.pathname.startsWith(item.href) && "bg-secondary")}
                                >
                                    <Icon className="mr-2 h-4 w-4" />
                                    {item.label}
                                </Button>
                            </Link>
                        );
                    })}
                </nav>
                <div className="p-4 border-t">
                    <Button variant="ghost" className="w-full justify-start text-red-500 hover:text-red-600 hover:bg-red-50">
                        <LogOut className="mr-2 h-4 w-4" />
                        Logout
                    </Button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                <header className="h-16 border-b flex items-center justify-between px-6">
                    <h2 className="font-semibold text-lg capitalize">{location.pathname.split('/')[1] || 'Dashboard'}</h2>
                    <div className="flex items-center gap-4">
                        <NotificationBell />
                        <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                            <span className="text-sm font-medium text-primary">JD</span>
                        </div>
                    </div>
                </header>
                <main className="flex-1 overflow-auto bg-gray-50/50">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
