import { useState } from "react";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Trash2, Download } from "lucide-react";
import type { AccountDocument } from "@/types/document";
import { format } from "date-fns";
import { documentService } from "@/services/documentService";

interface DocumentListProps {
    documents: AccountDocument[];
    onDeleteSuccess: () => void;
}

export function DocumentList({ documents, onDeleteSuccess }: DocumentListProps) {
    const [deletingId, setDeletingId] = useState<string | null>(null);

    const handleDelete = async (id: string) => {
        if (!confirm("Are you sure you want to delete this document?")) return;

        setDeletingId(id);
        try {
            await documentService.deleteDocument(id);
            onDeleteSuccess();
        } catch (error) {
            console.error("Failed to delete document", error);
            alert("Failed to delete document");
        } finally {
            setDeletingId(null);
        }
    };

    if (documents.length === 0) {
        return (
            <div className="text-center py-12 text-slate-500 bg-slate-50 rounded-lg border border-dashed">
                No documents uploaded yet.
            </div>
        );
    }

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Date Uploaded</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {documents.map((doc) => (
                    <TableRow key={doc.id}>
                        <TableCell className="font-medium flex items-center gap-2">
                            <span>📄</span>
                            {doc.name}
                        </TableCell>
                        <TableCell className="uppercase text-xs font-bold text-slate-500">
                            {doc.file_type || 'UNK'}
                        </TableCell>
                        <TableCell>
                            {format(new Date(doc.created_at), 'PPP')}
                        </TableCell>
                        <TableCell className="text-right">
                            <div className="flex justify-end gap-2">
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => window.open(`http://localhost:8000/${doc.file_path.replace('app/', '')}`, '_blank')}
                                >
                                    <Download className="h-4 w-4 text-slate-600" />
                                </Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => handleDelete(doc.id)}
                                    disabled={deletingId === doc.id}
                                >
                                    <Trash2 className="h-4 w-4 text-red-500" />
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    );
}
