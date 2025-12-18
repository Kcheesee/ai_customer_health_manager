import { useState, useEffect } from "react";
import { inputService } from "@/services/inputService";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Folder, Edit2, Check, X, Search } from "lucide-react";
import { format } from "date-fns";

export default function InputsPage() {
    const [inputs, setInputs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedFolder, setSelectedFolder] = useState<string>("All");
    const [editingId, setEditingId] = useState<string | null>(null);
    const [editValue, setEditValue] = useState("");

    useEffect(() => {
        fetchInputs();
    }, []);

    const fetchInputs = async () => {
        setLoading(true);
        try {
            const data = await inputService.getAllInputs();
            setInputs(data);
        } catch (err) {
            console.error("Failed to load inputs", err);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateFolder = async (id: string, newFolder: string) => {
        try {
            await inputService.updateInput(id, { folder: newFolder });
            setInputs(inputs.map(i => i.id === id ? { ...i, folder: newFolder } : i));
        } catch (err) {
            console.error("Update failed", err);
        }
    };

    const handleSaveEdit = async (id: string) => {
        try {
            await inputService.updateInput(id, { content: editValue });
            setInputs(inputs.map(i => i.id === id ? { ...i, content: editValue } : i));
            setEditingId(null);
        } catch (err) {
            console.error("Edit save failed", err);
        }
    };

    const folders = ["All", ...Array.from(new Set(inputs.filter(i => i.folder).map(i => i.folder)))];

    const filtered = inputs.filter(i => {
        const matchesSearch = i.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
            i.account_name?.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesFolder = selectedFolder === "All" || i.folder === selectedFolder;
        return matchesSearch && matchesFolder;
    });

    return (
        <div className="space-y-8 p-8 max-w-6xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-4xl font-black tracking-tight text-slate-900">Customer Intelligence</h1>
                    <p className="text-slate-500 mt-1">Global activity stream captured across all accounts.</p>
                </div>
            </div>

            <div className="flex flex-col md:flex-row gap-6">
                {/* Folder Sidebar */}
                <div className="w-full md:w-64 space-y-4">
                    <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400 px-2">Folders</h3>
                    <div className="space-y-1">
                        {folders.map(f => (
                            <button
                                key={f}
                                onClick={() => setSelectedFolder(f)}
                                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all ${selectedFolder === f ? 'bg-primary text-white font-bold' : 'text-slate-600 hover:bg-slate-100'}`}
                            >
                                <div className="flex items-center gap-2">
                                    <Folder className="h-4 w-4" />
                                    {f}
                                </div>
                                <span className="text-[10px] opacity-70">
                                    {f === "All" ? inputs.length : inputs.filter(i => i.folder === f).length}
                                </span>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="flex-1 space-y-6">
                    <div className="relative group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400 group-focus-within:text-primary transition-colors" />
                        <Input
                            placeholder="Search content or account names..."
                            className="pl-10 h-12 bg-white border-slate-200/60 focus-visible:ring-primary shadow-sm rounded-xl"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    {loading ? (
                        <div className="flex h-[400px] items-center justify-center">
                            <Loader2 className="h-8 w-8 animate-spin text-primary" />
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {filtered.length === 0 ? (
                                <Card className="border-2 border-dashed bg-slate-50/50">
                                    <CardContent className="py-24 text-center text-slate-500">
                                        No interactions found.
                                    </CardContent>
                                </Card>
                            ) : (
                                filtered.map((input) => (
                                    <Card key={input.id} className="group hover:shadow-lg transition-all border-none bg-white ring-1 ring-slate-200/60 overflow-hidden">
                                        <div className="p-6">
                                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                                                <div className="space-y-1">
                                                    <div className="flex items-center gap-2 mb-1">
                                                        <Badge variant="outline" className="text-[10px] font-bold uppercase tracking-wider bg-slate-50 border-slate-200">
                                                            {input.input_type.replace('_', ' ')}
                                                        </Badge>
                                                        <span className="text-[10px] font-bold text-slate-400 uppercase">
                                                            {format(new Date(input.content_date || input.created_at), "PPP")}
                                                        </span>
                                                    </div>
                                                    <h3 className="text-lg font-bold text-slate-900 group-hover:text-primary transition-colors flex items-center gap-2">
                                                        {input.account_name}
                                                        <span className="text-slate-300 font-normal">/</span>
                                                        <span className="text-slate-500 text-sm font-medium">{input.sender}</span>
                                                    </h3>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <div className="flex bg-slate-100 p-1 rounded-lg">
                                                        <button
                                                            onClick={() => {
                                                                const newFolder = prompt("Enter folder name:", input.folder || "");
                                                                if (newFolder !== null) handleUpdateFolder(input.id, newFolder);
                                                            }}
                                                            className="p-1 px-2 text-[10px] font-black uppercase text-slate-500 hover:text-primary hover:bg-white rounded transition-all flex items-center gap-1"
                                                        >
                                                            <Folder className="h-3 w-3" />
                                                            {input.folder || "Unorganized"}
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>

                                            {editingId === input.id ? (
                                                <div className="space-y-3">
                                                    <textarea
                                                        className="w-full p-4 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary outline-none transition-all min-h-[120px]"
                                                        value={editValue}
                                                        onChange={(e) => setEditValue(e.target.value)}
                                                    />
                                                    <div className="flex gap-2">
                                                        <Button size="sm" onClick={() => handleSaveEdit(input.id)}>
                                                            <Check className="h-4 w-4 mr-1" /> Save
                                                        </Button>
                                                        <Button size="sm" variant="ghost" onClick={() => setEditingId(null)}>
                                                            <X className="h-4 w-4 mr-1" /> Cancel
                                                        </Button>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="relative group/content">
                                                    <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap line-clamp-4">
                                                        {input.content}
                                                    </p>
                                                    <button
                                                        onClick={() => {
                                                            setEditingId(input.id);
                                                            setEditValue(input.content);
                                                        }}
                                                        className="absolute -right-2 -top-2 p-2 bg-white shadow-md rounded-full text-slate-400 opacity-0 group/content-hover:opacity-100 hover:text-primary transition-all border border-slate-100"
                                                    >
                                                        <Edit2 className="h-3 w-3" />
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </Card>
                                ))
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
