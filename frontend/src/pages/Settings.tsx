import { useEffect, useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { LLMConfig, LLMProviderType } from "@/types/llm";
import { llmService } from "@/services/llmService";

export default function SettingsPage() {
    const [configs, setConfigs] = useState<LLMConfig[]>([]); // Keep as array for compatibility if we expand later, but currently single

    // Form State
    const [provider, setProvider] = useState<LLMProviderType>('anthropic');
    const [modelName, setModelName] = useState("");
    const [apiKey, setApiKey] = useState("");
    const [loading, setLoading] = useState(false);

    console.log("SettingsPage Render: ", { provider, loading, configsLen: configs.length });

    useEffect(() => {
        loadConfig();
    }, []);

    const loadConfig = async () => {
        try {
            const data = await llmService.getConfig();
            console.log("SettingsPage loadConfig success:", data);
            setConfigs([data]); // Wrap in array to satisfy type if needed, or simplifiy.

            // Populate form
            setProvider(data.provider);
            setModelName(data.model_name);
            // Don't populate API Key (security), stick to placeholder state logic
            setApiKey("");
        } catch (error) {
            console.error(error);
        }
    };

    const handleTest = async () => {
        setLoading(true);
        try {
            const res = await llmService.testConnection({
                provider,
                model_name: modelName,
                api_key: apiKey || undefined
            });
            alert(`Connection Successful! Response: "${res.response}"`);
        } catch (error: any) {
            console.error(error);
            alert(`Connection Failed: ${error.message || "Unknown error"}`);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            await llmService.updateConfig({
                provider,
                model_name: modelName,
                api_key: apiKey || undefined, // Only send if set
                is_active: true
            });
            // Clear API key input after save
            setApiKey("");
            await loadConfig();
            alert("Configuration saved!");
        } catch (error) {
            console.error(error);
            alert("Failed to save configuration.");
        } finally {
            setLoading(false);
        }
    };



    return (
        <div className="flex-1 space-y-4 p-8 pt-6">
            <div className="flex items-center justify-between space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
            </div>

            <Tabs defaultValue="llm" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="llm">LLM Configuration</TabsTrigger>
                    <TabsTrigger value="notifications">Notifications</TabsTrigger>
                </TabsList>

                <TabsContent value="llm" className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">

                        <Card className="col-span-4">
                            <CardHeader>
                                <CardTitle>LLM Configuration</CardTitle>
                                <CardDescription>
                                    Configure the AI provider. API Keys are encrypted at rest.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-1">
                                    <Label htmlFor="provider">Provider</Label>
                                    <Select value={provider} onValueChange={(val: LLMProviderType) => setProvider(val)}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select provider" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="anthropic">Anthropic</SelectItem>
                                            <SelectItem value="openai">OpenAI</SelectItem>
                                            <SelectItem value="google">Google Gemini</SelectItem>
                                            <SelectItem value="mock">Mock Provider</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="space-y-1">
                                    <Label htmlFor="model">Model Name</Label>
                                    <Input
                                        id="model"
                                        placeholder="e.g. gpt-4 or claude-3-opus"
                                        value={modelName}
                                        onChange={(e) => setModelName(e.target.value)}
                                    />
                                </div>
                                <div className="space-y-1">
                                    <Label htmlFor="apikey">API Key</Label>
                                    <Input
                                        id="apikey"
                                        type="password"
                                        placeholder={apiKey ? "********" : "Enter API Key"}
                                        value={apiKey}
                                        onChange={(e) => setApiKey(e.target.value)}
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        {configs.length > 0 && configs[0].api_key_masked ? "API Key is set." : "No API Key set."}
                                    </p>
                                </div>
                            </CardContent>
                            <CardFooter className="flex justify-between">
                                <Button variant="outline" onClick={handleTest} disabled={loading}>
                                    Test Connection
                                </Button>
                                <Button onClick={handleSave} disabled={loading}>
                                    {loading ? "Saving..." : "Save Configuration"}
                                </Button>
                            </CardFooter>
                        </Card>

                    </div>
                </TabsContent>

                <TabsContent value="notifications">
                    <Card>
                        <CardHeader>
                            <CardTitle>Notifications</CardTitle>
                            <CardDescription>Configure alerts and email settings.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p>Coming soon...</p>
                        </CardContent>
                    </Card>
                </TabsContent>

            </Tabs>
        </div>
    );
}
