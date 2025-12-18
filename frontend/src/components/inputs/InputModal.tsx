import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { InputCreate } from "@/types/input";
import { inputService } from "@/services/inputService";
import { Plus } from "lucide-react";

interface InputModalProps {
    accountId: string;
    onSuccess?: () => void;
}

export function InputModal({ accountId, onSuccess }: InputModalProps) {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<Partial<InputCreate>>({
        input_type: "email",
        content: "",
        sender: "",
        content_date: new Date().toISOString().split('T')[0], // Default to today
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.content?.trim()) {
            alert("Content is required");
            return;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (formData.sender && !emailRegex.test(formData.sender)) {
            alert("Please enter a valid email for the sender");
            return;
        }

        setLoading(true);
        try {
            await inputService.createInput({
                account_id: accountId,
                content: formData.content!,
                input_type: formData.input_type as any,
                sender: formData.sender,
                content_date: formData.content_date,
            });
            setOpen(false);
            setFormData({
                input_type: "email",
                content: "",
                sender: "",
                content_date: new Date().toISOString().split('T')[0]
            });
            if (onSuccess) onSuccess();
        } catch (error) {
            console.error("Failed to add input", error);
            alert("Failed to add input. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button size="sm"><Plus className="mr-2 h-4 w-4" /> Add Input</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <form onSubmit={handleSubmit}>
                    <DialogHeader>
                        <DialogTitle>Add Customer Input</DialogTitle>
                        <DialogDescription>
                            Paste an email, ticket, or call note here. The AI will analyze it automatically.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="type" className="text-right">
                                Type
                            </Label>
                            <Select
                                value={formData.input_type}
                                onValueChange={(val) => setFormData({ ...formData, input_type: val as any })}
                            >
                                <SelectTrigger className="col-span-3">
                                    <SelectValue placeholder="Select type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="email">Email</SelectItem>
                                    <SelectItem value="ticket">Ticket</SelectItem>
                                    <SelectItem value="call">Call Note</SelectItem>
                                    <SelectItem value="meeting_note">Meeting Note</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="sender" className="text-right">
                                Sender
                            </Label>
                            <Input
                                id="sender"
                                placeholder="email@example.com"
                                className="col-span-3"
                                value={formData.sender}
                                onChange={(e) => setFormData({ ...formData, sender: e.target.value })}
                            />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="date" className="text-right">
                                Date
                            </Label>
                            <Input
                                id="date"
                                type="date"
                                className="col-span-3"
                                value={formData.content_date}
                                onChange={(e) => setFormData({ ...formData, content_date: e.target.value })}
                            />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="content" className="text-right">
                                Content
                            </Label>
                            <Textarea
                                id="content"
                                placeholder="Paste content here..."
                                className="col-span-3 min-h-[100px]"
                                value={formData.content}
                                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                                required
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button type="submit" disabled={loading}>
                            {loading ? "Analyzing..." : "Save Input"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
