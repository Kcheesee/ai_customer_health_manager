import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import type { Account } from "@/types/account";
import type { HealthScore } from "@/types/health";
import type { Input as InputType } from "@/types/input";
import type { Contract } from "@/types/contract"; // Add Contract type
import { accountService } from "@/services/accountService";
import { healthService } from "@/services/healthService";
import { inputService } from "@/services/inputService";
import { contractService } from "@/services/contractService"; // Add contractService
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { HealthBadge } from "@/components/health/HealthBadge";
import { ArrowLeft, RefreshCw } from "lucide-react";
import { ReminderList } from "@/components/reminders/ReminderList";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { InputModal } from "@/components/inputs/InputModal";
import { ContractList } from "@/components/contracts/ContractList"; // Add ContractList
import { ContractModal } from "@/components/contracts/ContractModal"; // Add ContractModal
import { format } from "date-fns";

export default function AccountDetail() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [account, setAccount] = useState<Account | null>(null);
    const [healthScore, setHealthScore] = useState<HealthScore | null>(null);
    const [inputs, setInputs] = useState<InputType[]>([]);
    const [contracts, setContracts] = useState<Contract[]>([]);
    const [children, setChildren] = useState<Account[]>([]); // Add children state
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null); // Add error state
    const [recalculating, setRecalculating] = useState(false);
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const [isContractModalOpen, setIsContractModalOpen] = useState(false); // Add modal state

    useEffect(() => {
        if (id) {
            fetchData();
        }
    }, [id, refreshTrigger]);

    const fetchData = async () => {
        if (!id) return;
        setLoading(true);
        try {
            const [accData, healthData, inputsData, contractsData, childrenData] = await Promise.all([
                accountService.getAccount(id),
                healthService.getLatestHealth(id),
                inputService.getInputs(id),
                contractService.getContracts(id),
                accountService.getChildren(id) // Fetch children
            ]);
            setAccount(accData);
            setHealthScore(healthData);
            setInputs(inputsData);
            setContracts(contractsData);
            setChildren(childrenData); // Set children
        } catch (error: any) {
            console.error("Failed to fetch account details", error);
            setError(error.message || "An unexpected error occurred while loading account data.");
        } finally {
            setLoading(false);
        }
    };

    const handleRecalculate = async () => {
        if (!id) return;
        setRecalculating(true);
        try {
            const newHealth = await healthService.calculateScore(id);
            setHealthScore(newHealth);
        } catch (error) {
            console.error(error);
        } finally {
            setRecalculating(false);
        }
    };

    if (loading) return (
        <div className="space-y-6 p-8 animate-pulse">
            <div className="flex justify-between items-center">
                <div className="h-8 w-64 bg-slate-200 rounded"></div>
                <div className="h-8 w-32 bg-slate-200 rounded"></div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="h-96 bg-slate-100 rounded"></div>
                <div className="md:col-span-2 h-96 bg-slate-100 rounded"></div>
            </div>
        </div>
    );

    if (error) return (
        <div className="p-8 text-center">
            <Card className="border-red-200 bg-red-50">
                <CardContent className="py-12">
                    <div className="text-red-500 font-bold mb-2">Error Loading Account</div>
                    <div className="text-sm text-red-700 mb-4">{error}</div>
                    <Button onClick={() => { setError(null); setRefreshTrigger(p => p + 1); }}>Try Again</Button>
                </CardContent>
            </Card>
        </div>
    );

    if (!account) return <div className="p-8 text-center">Account not found</div>;

    return (
        <div className="space-y-10 p-10 max-w-7xl mx-auto">
            {/* Action Header */}
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div className="flex items-center gap-6">
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => navigate("/accounts")}
                        className="rounded-full bg-white shadow-sm ring-1 ring-slate-200 hover:ring-primary/50 transition-all"
                    >
                        <ArrowLeft className="h-5 w-5 text-slate-600" />
                    </Button>
                    <div>
                        <div className="flex items-center gap-3 mb-2">
                            <h2 className="text-4xl font-black tracking-tight text-slate-900">{account.name}</h2>
                            <div className="flex gap-2">
                                <Badge variant="secondary" className="px-3 py-1 text-[10px] font-bold uppercase tracking-widest bg-slate-100 text-slate-500 border-none">
                                    {account.account_type.replace("_", " ")}
                                </Badge>
                                <Badge className="px-3 py-1 text-[10px] font-bold uppercase tracking-widest bg-primary text-white border-none">
                                    {account.tier}
                                </Badge>
                            </div>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-slate-500 font-medium">
                            <span className="flex h-2 w-2 rounded-full bg-green-500"></span>
                            Active Account • {account.industry || "General Industry"}
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-4 bg-white/50 backdrop-blur-sm p-4 rounded-3xl ring-1 ring-slate-200 shadow-xl">
                    <div className="text-right">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest leading-none mb-1">Live Health Pulse</div>
                        <div className="text-lg font-black text-slate-900">Aggregate Status</div>
                    </div>
                    {healthScore && <HealthBadge score={healthScore.overall_score} status={healthScore.overall_status} size="lg" className="scale-110" />}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
                {/* Left Column: Health & Stats - 4 cols */}
                <div className="lg:col-span-4 space-y-8">
                    {/* Main Health Card */}
                    <Card className="border-none bg-slate-900 text-white shadow-2xl overflow-hidden relative group">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/20 blur-3xl -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-700" />
                        <CardHeader className="pb-2">
                            <CardTitle className="text-xs font-bold uppercase tracking-widest text-slate-400">Pillar Performance</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6 pt-4">
                            {healthScore ? (
                                <>
                                    {/* AI Summary in a premium box */}
                                    {healthScore.ai_summary && (
                                        <div className="relative">
                                            <div className="absolute -left-3 top-0 bottom-0 w-1 bg-primary rounded-full"></div>
                                            <p className="text-sm text-slate-200 font-medium leading-relaxed italic pl-3">
                                                "{healthScore.ai_summary}"
                                            </p>
                                        </div>
                                    )}

                                    <div className="grid grid-cols-2 gap-4">
                                        {[
                                            { label: 'Sentiment', val: healthScore.sentiment_score },
                                            { label: 'Engagement', val: healthScore.engagement_score },
                                            { label: 'Requests', val: healthScore.request_score },
                                            { label: 'Satisfaction', val: healthScore.satisfaction_score },
                                        ].map(stat => (
                                            <div key={stat.label} className="bg-white/5 rounded-2xl p-4 border border-white/10">
                                                <div className="text-[10px] font-bold text-slate-400 uppercase mb-1">{stat.label}</div>
                                                <div className="text-xl font-black">{stat.val}%</div>
                                                <div className="h-1 w-full bg-white/10 rounded-full mt-2 overflow-hidden">
                                                    <div className="h-full bg-primary" style={{ width: `${stat.val}%` }}></div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    <Button
                                        variant="default"
                                        className="w-full h-12 rounded-2xl font-bold bg-white text-slate-900 hover:bg-slate-100 transition-all shadow-lg"
                                        onClick={handleRecalculate}
                                        disabled={recalculating}
                                    >
                                        <RefreshCw className={`mr-2 h-4 w-4 ${recalculating ? 'animate-spin' : ''}`} />
                                        {recalculating ? "Processing Analytis..." : "Update Intelligence"}
                                    </Button>
                                </>
                            ) : (
                                <div className="text-center py-8">
                                    <Button variant="outline" className="text-white border-white/20 hover:bg-white/10" onClick={handleRecalculate}>Begin Health Analysis</Button>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Meta Stats Cards */}
                    <div className="grid grid-cols-1 gap-4">
                        <Card className="border-none shadow-sm ring-1 ring-slate-200 bg-white/50">
                            <CardContent className="p-6">
                                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Account Metadata</div>
                                <div className="space-y-4">
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm font-medium text-slate-500">Industry Focal</span>
                                        <span className="text-sm font-black text-slate-900">{account.industry || "N/A"}</span>
                                    </div>
                                    <div className="flex justify-between items-center text-sm">
                                        <span className="font-medium text-slate-500">Cadence</span>
                                        <Badge variant="outline" className="font-bold">{account.check_in_interval_days} Days</Badge>
                                    </div>
                                    <div className="flex justify-between items-center text-sm">
                                        <span className="font-medium text-slate-500">Tenure</span>
                                        <span className="font-bold text-slate-900">{format(new Date(account.created_at || Date.now()), 'MMM yyyy')}</span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Reminders / Commitments */}
                        <Card className="border-none shadow-sm ring-1 ring-slate-200 bg-white group">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-xs font-bold uppercase tracking-widest text-slate-400">Priority Commitments</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <ReminderList accountId={account.id} />
                            </CardContent>
                        </Card>
                    </div>
                </div>

                {/* Right Column: Activity Stream & Inputs - 8 cols */}
                <div className="lg:col-span-8">
                    <Tabs defaultValue="activity" className="w-full">
                        <div className="flex items-center justify-between mb-8">
                            <TabsList className="bg-slate-100 p-1 rounded-2xl">
                                <TabsTrigger value="activity" className="rounded-xl px-6 py-2.5 data-[state=active]:bg-white data-[state=active]:shadow-sm font-bold text-sm">Activity</TabsTrigger>
                                <TabsTrigger value="contracts" className="rounded-xl px-6 py-2.5 data-[state=active]:bg-white data-[state=active]:shadow-sm font-bold text-sm">Contracts</TabsTrigger>
                                {account.account_type === "ela_parent" && (
                                    <TabsTrigger value="offices" className="rounded-xl px-6 py-2.5 data-[state=active]:bg-white data-[state=active]:shadow-sm font-bold text-sm">Offices</TabsTrigger>
                                )}
                            </TabsList>

                            <TabsContent value="activity" className="m-0">
                                <InputModal accountId={id!} onSuccess={() => setRefreshTrigger(prev => prev + 1)} />
                            </TabsContent>
                        </div>

                        <TabsContent value="activity" className="space-y-6 m-0 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            {inputs.length === 0 ? (
                                <div className="py-32 text-center bg-slate-50 border-2 border-dashed rounded-3xl">
                                    <div className="bg-white p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center shadow-lg">
                                        <RefreshCw className="text-slate-300" />
                                    </div>
                                    <h3 className="font-bold text-slate-800">No Intelligence Captured</h3>
                                    <p className="text-sm text-slate-500 mt-1">Start by adding a meeting note or email thread.</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {inputs.map((input) => (
                                        <Card key={input.id} className="border-none ring-1 ring-slate-200/60 shadow-sm hover:shadow-xl transition-all duration-300 bg-white overflow-hidden group">
                                            <div className="h-1 w-full bg-slate-50 group-hover:bg-primary transition-colors"></div>
                                            <CardHeader className="py-5">
                                                <div className="flex justify-between items-start">
                                                    <div>
                                                        <div className="flex items-center gap-2 mb-2">
                                                            <Badge variant="outline" className="text-[10px] font-black uppercase tracking-widest bg-slate-50 border-slate-200">
                                                                {input.input_type.replace('_', ' ')}
                                                            </Badge>
                                                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">
                                                                {format(new Date(input.content_date || input.created_at || Date.now()), 'PPP')}
                                                            </span>
                                                        </div>
                                                        <CardTitle className="text-lg font-bold text-slate-900">
                                                            Message from {input.sender}
                                                        </CardTitle>
                                                    </div>
                                                </div>
                                            </CardHeader>
                                            <CardContent className="pb-5 pt-0 text-sm text-slate-600 leading-relaxed font-medium">
                                                <div className="bg-slate-50/50 p-4 rounded-xl border border-slate-100">
                                                    {input.content}
                                                </div>
                                            </CardContent>
                                        </Card>
                                    ))}
                                </div>
                            )}
                        </TabsContent>

                        <TabsContent value="contracts" className="m-0 space-y-6">
                            <div className="bg-white rounded-3xl ring-1 ring-slate-200 p-8 shadow-sm">
                                <ContractList
                                    contracts={contracts}
                                    onAddContract={() => setIsContractModalOpen(true)}
                                />
                            </div>
                        </TabsContent>

                        <TabsContent value="offices" className="m-0 space-y-6">
                            <div className="flex justify-between items-center">
                                <h3 className="text-2xl font-black text-slate-900 tracking-tight">Enterprise Hierarchy</h3>
                                <Button
                                    className="rounded-xl font-bold"
                                    onClick={() => navigate(`/accounts/new?parent_id=${id}`)}
                                >
                                    Register New Office
                                </Button>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {children.length === 0 ? (
                                    <div className="col-span-2 py-20 text-center bg-slate-50 border-2 border-dashed rounded-3xl text-slate-400">
                                        No linked child accounts detected.
                                    </div>
                                ) : (
                                    children.map(child => (
                                        <Card key={child.id} className="hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 border-none ring-1 ring-slate-200 bg-white cursor-pointer group" onClick={() => navigate(`/accounts/${child.id}`)}>
                                            <CardContent className="p-6">
                                                <div className="flex justify-between items-start">
                                                    <div>
                                                        <div className="text-lg font-black text-slate-900 group-hover:text-primary transition-colors">{child.name}</div>
                                                        <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">{child.tier} • {child.industry}</div>
                                                    </div>
                                                    <div className="bg-slate-50 p-2 rounded-xl text-slate-400 group-hover:bg-primary group-hover:text-white transition-all">
                                                        <ArrowLeft className="h-4 w-4 rotate-180" />
                                                    </div>
                                                </div>
                                            </CardContent>
                                        </Card>
                                    ))
                                )}
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>

            <ContractModal
                accountId={id!}
                isOpen={isContractModalOpen}
                onClose={() => setIsContractModalOpen(false)}
                onSuccess={() => setRefreshTrigger(prev => prev + 1)}
            />
        </div>
    );
}
