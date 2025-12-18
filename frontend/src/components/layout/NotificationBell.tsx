import { useEffect, useState } from "react";
import { Bell, Check, Info, AlertTriangle, XCircle } from "lucide-react";
import type { Alert } from "@/types/alert";
import { alertService } from "@/services/alertService";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useNavigate } from "react-router-dom";

export function NotificationBell() {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);
    const navigate = useNavigate();

    const fetchAlerts = async () => {
        try {
            const data = await alertService.getAlerts();
            setAlerts(data);
            setUnreadCount(data.filter(a => !a.is_read).length);
        } catch (error) {
            console.error("Failed to fetch alerts:", error);
        }
    };

    useEffect(() => {
        fetchAlerts();
        // Poll every 60 seconds
        const interval = setInterval(fetchAlerts, 60000);
        return () => clearInterval(interval);
    }, []);

    const handleMarkAsRead = async (alert: Alert) => {
        if (!alert.is_read) {
            try {
                await alertService.markAsRead(alert.id);
                fetchAlerts();
            } catch (error) {
                console.error("Failed to mark as read:", error);
            }
        }
    };

    const handleMarkAllRead = async () => {
        try {
            await alertService.markAllRead();
            fetchAlerts();
        } catch (error) {
            console.error(error);
        }
    }

    const handleClick = (alert: Alert) => {
        handleMarkAsRead(alert);
        if (alert.link) {
            setIsOpen(false);
            navigate(alert.link);
        }
    };

    const getIcon = (type: string) => {
        switch (type) {
            case "error": return <XCircle className="h-4 w-4 text-red-500" />;
            case "warning": return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
            case "success": return <Check className="h-4 w-4 text-green-500" />;
            default: return <Info className="h-4 w-4 text-blue-500" />;
        }
    };

    return (
        <Popover open={isOpen} onOpenChange={setIsOpen}>
            <PopoverTrigger asChild>
                <Button variant="ghost" size="icon" className="relative">
                    <Bell className="h-5 w-5" />
                    {unreadCount > 0 && (
                        <span className="absolute top-0 right-0 h-4 w-4 bg-red-500 rounded-full text-[10px] text-white flex items-center justify-center font-bold">
                            {unreadCount > 9 ? "9+" : unreadCount}
                        </span>
                    )}
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-80 p-0" align="end">
                <div className="flex items-center justify-between p-4 border-b">
                    <h4 className="font-semibold text-sm">Notifications</h4>
                    {unreadCount > 0 && (
                        <Button variant="ghost" size="sm" className="text-xs h-auto p-1 text-muted-foreground" onClick={handleMarkAllRead}>
                            Mark all read
                        </Button>
                    )}
                </div>
                <ScrollArea className="h-80">
                    {alerts.length === 0 ? (
                        <div className="p-4 text-center text-sm text-muted-foreground">
                            No notifications
                        </div>
                    ) : (
                        <div className="divide-y relative">
                            {alerts.map((alert) => (
                                <div
                                    key={alert.id}
                                    className={`p-4 flex gap-3 hover:bg-muted/50 cursor-pointer transition-colors ${!alert.is_read ? "bg-muted/20" : ""}`}
                                    onClick={() => handleClick(alert)}
                                >
                                    <div className="mt-1 flex-shrink-0">
                                        {getIcon(alert.type)}
                                    </div>
                                    <div className="space-y-1 flex-1">
                                        <div className="flex justify-between items-start gap-2">
                                            <p className={`text-sm font-medium leading-none ${!alert.is_read ? "text-foreground" : "text-muted-foreground"}`}>
                                                {alert.title}
                                            </p>
                                            {!alert.is_read && (
                                                <div className="min-w-[6px] w-[6px] h-[6px] rounded-full bg-blue-500 mt-1" />
                                            )}
                                        </div>
                                        <p className="text-xs text-muted-foreground line-clamp-2">
                                            {alert.message}
                                        </p>
                                        <p className="text-[10px] text-muted-foreground/70">
                                            {new Date(alert.created_at).toLocaleString()}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </ScrollArea>
            </PopoverContent>
        </Popover>
    );
}
