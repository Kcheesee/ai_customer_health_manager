import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
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

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-lg font-medium">Contracts</CardTitle>
                <Button size="sm" onClick={onAddContract}>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Contract
                </Button>
            </CardHeader>
            <CardContent>
                {contracts.length === 0 ? (
                    <div className="text-center py-8 text-gray-500 text-sm">
                        No contracts found for this account.
                    </div>
                ) : (
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>End Date</TableHead>
                                <TableHead>ARR</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {contracts.map((contract) => (
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
                            ))}
                        </TableBody>
                    </Table>
                )}
            </CardContent>
        </Card>
    );
}
