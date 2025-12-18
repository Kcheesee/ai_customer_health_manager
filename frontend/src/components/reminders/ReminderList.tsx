import { useState, useEffect } from "react";
import { reminderService } from "@/services/reminderService";
import type { Reminder } from "@/services/reminderService";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Calendar, Trash2, Plus } from "lucide-react";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar as CalendarComponent } from "@/components/ui/calendar";
import { format } from "date-fns";

interface ReminderListProps {
    accountId: string;
}

export function ReminderList({ accountId }: ReminderListProps) {
    const [reminders, setReminders] = useState<Reminder[]>([]);
    const [newReminderText, setNewReminderText] = useState("");
    const [newReminderDate, setNewReminderDate] = useState<Date | undefined>(undefined);
    const [isLoading, setIsLoading] = useState(false);

    const fetchReminders = async () => {
        try {
            const data = await reminderService.getReminders(accountId);
            setReminders(data);
        } catch (error) {
            console.error("Failed to fetch reminders", error);
        }
    };

    useEffect(() => {
        fetchReminders();
    }, [accountId]);

    const handleToggle = async (id: string, currentStatus: boolean) => {
        // Optimistic update
        setReminders(reminders.map(r => r.id === id ? { ...r, is_completed: !currentStatus } : r));
        try {
            await reminderService.updateReminder(id, { is_completed: !currentStatus });
        } catch (error) {
            fetchReminders(); // Revert on error
        }
    };

    const handleDelete = async (id: string) => {
        setReminders(reminders.filter(r => r.id !== id));
        try {
            await reminderService.deleteReminder(id);
        } catch (error) {
            fetchReminders();
        }
    };

    const handleAdd = async () => {
        if (!newReminderText.trim()) return;
        setIsLoading(true);
        try {
            const newReminder = await reminderService.createReminder(accountId, newReminderText, newReminderDate);
            setReminders([newReminder, ...reminders]);
            setNewReminderText("");
            setNewReminderDate(undefined);
        } catch (error) {
            console.error("Failed to create reminder", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="space-y-4">
            <h3 className="font-semibold text-lg flex items-center gap-2">
                <Check className="h-5 w-5 text-primary" />
                Reminders & Commitments
            </h3>

            {/* Add New */}
            <div className="flex gap-2">
                <Input
                    placeholder="Add a new task..."
                    value={newReminderText}
                    onChange={(e) => setNewReminderText(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleAdd()}
                />
                <Popover>
                    <PopoverTrigger asChild>
                        <Button variant="outline" size="icon" className={newReminderDate ? "text-primary border-primary" : "text-muted-foreground"}>
                            <Calendar className="h-4 w-4" />
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="end">
                        <CalendarComponent
                            mode="single"
                            selected={newReminderDate}
                            onSelect={setNewReminderDate}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Button onClick={handleAdd} disabled={isLoading || !newReminderText.trim()}>
                    <Plus className="h-4 w-4" />
                </Button>
            </div>

            {/* List */}
            <div className="space-y-2">
                {reminders.length === 0 && (
                    <div className="text-sm text-muted-foreground text-center py-4">
                        No reminders yet.
                    </div>
                )}
                {reminders.map((reminder) => (
                    <div key={reminder.id} className="flex items-start gap-3 p-3 rounded-lg border bg-card hover:bg-accent/5 transition-colors group">
                        <Checkbox
                            checked={reminder.is_completed}
                            onCheckedChange={() => handleToggle(reminder.id, reminder.is_completed)}
                            className="mt-1"
                        />
                        <div className="flex-1 space-y-1">
                            <p className={`text-sm ${reminder.is_completed ? "line-through text-muted-foreground" : "font-medium"}`}>
                                {reminder.description}
                            </p>
                            {reminder.due_date && (
                                <p className="text-xs text-muted-foreground flex items-center gap-1">
                                    <Calendar className="h-3 w-3" />
                                    {format(new Date(reminder.due_date), "MMM d, yyyy")}
                                </p>
                            )}
                        </div>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-red-500"
                            onClick={() => handleDelete(reminder.id)}
                        >
                            <Trash2 className="h-3 w-3" />
                        </Button>
                    </div>
                ))}
            </div>
        </div>
    );
}

import { Check } from "lucide-react";
