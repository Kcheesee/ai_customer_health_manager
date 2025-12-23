import { useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import type { Contract } from "@/types/contract";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface ContractListProps {
    contracts: Contract[];
    onAddContract: () => void;
}

export function ContractList({ contracts, onAddContract }: ContractListProps) {
    const getStatusColor = (status: string) => {
        switch (status.toLowerCase()) {
            case "active":
                return "bg-green-100 text-green-800 hover:bg-green-100";
            case "expired":
                return "bg-red-100 text-red-800 hover:bg-red-100";
            case "pending_renewal":
                return "bg-yellow-100 text-yellow-800 hover:bg-yellow-100";
            case "draft":
                return "bg-gray-100 text-gray-800 hover:bg-gray-100";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };

    const formatCurrency = (val?: number) => {
        if (val === undefined || val === null) return "-";
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 0,
        }).format(val);
    };

    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleDateString();
    };

    const [searchQuery, setSearchQuery] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    const [typeFilter, setTypeFilter] = useState("all");
    const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);

    // Get unique types for filter
    const contractTypes = Array.from(new Set(contracts.map(c => c.contract_type))).filter(Boolean);

    const handleSort = (key: string) => {
        let direction: 'asc' | 'desc' = 'asc';
        if (sortConfig && sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    const sortedAndFilteredContracts = contracts
        .filter(contract => {
            const matchesSearch = contract.contract_name.toLowerCase().includes(searchQuery.toLowerCase());
            const matchesStatus = statusFilter === "all" || contract.status === statusFilter;
            const matchesType = typeFilter === "all" || contract.contract_type === typeFilter;
            return matchesSearch && matchesStatus && matchesType;
        })
        .sort((a, b) => {
            if (!sortConfig) return 0;
            const { key, direction } = sortConfig;

            let aValue: any = (a as any)[key];
            let bValue: any = (b as any)[key];

            if (key === 'arr') {
                aValue = Number(aValue || 0);
                bValue = Number(bValue || 0);
            }

            if (aValue < bValue) return direction === 'asc' ? -1 : 1;
            if (aValue > bValue) return direction === 'asc' ? 1 : -1;
            return 0;
        });

    return (
        <Card>
            <CardHeader>
                <div className="flex flex-row items-center justify-between pb-4">
                    <CardTitle className="text-lg font-medium">Contracts</CardTitle>
                    <Button size="sm" onClick={onAddContract}>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Contract
                    </Button>
                </div>

                {/* Filters */}
                <div className="flex gap-4">
                    <div className="flex-1">
                        <Input
                            placeholder="Search contracts..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="max-w-sm"
                        />
                    </div>
                    <Select value={statusFilter} onValueChange={setStatusFilter}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Filter Status" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">All Statuses</SelectItem>
                            <SelectItem value="active">Active</SelectItem>
                            <SelectItem value="expired">Expired</SelectItem>
                            <SelectItem value="pending_renewal">Pending Renewal</SelectItem>
                            <SelectItem value="draft">Draft</SelectItem>
                        </SelectContent>
                    </Select>
                    <Select value={typeFilter} onValueChange={setTypeFilter}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Filter Type" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">All Types</SelectItem>
                            {contractTypes.map(t => (
                                <SelectItem key={t} value={t} className="capitalize">
                                    {t.replace('_', ' ')}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
            </CardHeader>
            <CardContent>
                {sortedAndFilteredContracts.length === 0 ? (
                    <div className="text-center py-8 text-gray-500 text-sm">
                        No contracts found matching your filters.
                    </div>
                ) : (
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead className="cursor-pointer hover:bg-slate-50" onClick={() => handleSort('contract_name')}>
                                    Name {sortConfig?.key === 'contract_name' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                </TableHead>
                                <TableHead className="cursor-pointer hover:bg-slate-50" onClick={() => handleSort('contract_type')}>
                                    Type {sortConfig?.key === 'contract_type' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                </TableHead>
                                <TableHead className="cursor-pointer hover:bg-slate-50" onClick={() => handleSort('status')}>
                                    Status {sortConfig?.key === 'status' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                </TableHead>
                                <TableHead className="cursor-pointer hover:bg-slate-50" onClick={() => handleSort('end_date')}>
                                    End Date {sortConfig?.key === 'end_date' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                </TableHead>
                                <TableHead className="cursor-pointer hover:bg-slate-50" onClick={() => handleSort('arr')}>
                                    ARR {sortConfig?.key === 'arr' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                </TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {sortedAndFilteredContracts.map((contract) => (
                                <>
                                    <TableRow key={contract.id}>
                                        <TableCell className="font-medium">{contract.contract_name}</TableCell>
                                        <TableCell className="capitalize">{contract.contract_type?.replace('_', ' ')}</TableCell>
                                        <TableCell>
                                            <Badge className={getStatusColor(contract.status)} variant="secondary">
                                                {contract.status.replace('_', ' ')}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>{formatDate(contract.end_date)}</TableCell>
                                        <TableCell>{formatCurrency(contract.arr)}</TableCell>
                                        <TableCell className="text-right">
                                            <DropdownMenu>
                                                <DropdownMenuTrigger asChild>
                                                    <Button variant="ghost" className="h-8 w-8 p-0">
                                                        <span className="sr-only">Open menu</span>
                                                        <span className="h-4 w-4">...</span>
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem>View details</DropdownMenuItem>
                                                    <DropdownMenuItem>Edit contract</DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
                                        </TableCell>
                                    </TableRow>
                                    {(contract.full_text || contract.document_path) && (
                                        <TableRow>
                                            <TableCell colSpan={6} className="bg-slate-50 p-4">
                                                <div className="text-sm text-slate-600">
                                                    <h4 className="font-semibold mb-2">Contract Details:</h4>

                                                    {contract.document_path && (
                                                        <div className="mb-4">
                                                            <a
                                                                href={`http://localhost:8000/${contract.document_path.replace('app/', '')}`}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                className="text-blue-600 hover:underline flex items-center font-medium"
                                                            >
                                                                📄 Download / View Attached Document
                                                            </a>
                                                        </div>
                                                    )}

                                                    {contract.full_text && (
                                                        <>
                                                            <h5 className="font-medium mb-1 text-slate-500">Full Text / Notes:</h5>
                                                            <pre className="whitespace-pre-wrap font-sans bg-white p-3 rounded border">
                                                                {contract.full_text}
                                                            </pre>
                                                        </>
                                                    )}
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    )}
                                </>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </CardContent>
        </Card>
    );
}
