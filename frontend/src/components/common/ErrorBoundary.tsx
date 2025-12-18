import { Component, type ErrorInfo, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertTriangle } from "lucide-react";

interface Props {
    children?: ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false
    };

    public static getDerivedStateFromError(error: Error): State {
        // Update state so the next render will show the fallback UI.
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error("Uncaught error:", error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen flex items-center justify-center p-4 bg-slate-50">
                    <Card className="max-w-md w-full border-red-200">
                        <CardHeader>
                            <div className="flex items-center gap-2 text-red-600 mb-2">
                                <AlertTriangle className="h-6 w-6" />
                                <CardTitle>Something went wrong</CardTitle>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <p className="text-sm text-slate-600 mb-4">
                                The application encountered an unexpected error. Please try refreshing the page or contact support if the problem persists.
                            </p>
                            {this.state.error && (
                                <div className="bg-slate-100 p-3 rounded text-xs font-mono text-slate-700 overflow-auto max-h-32 mb-4">
                                    {this.state.error.toString()}
                                </div>
                            )}
                        </CardContent>
                        <CardFooter>
                            <Button
                                className="w-full"
                                onClick={() => window.location.reload()}
                            >
                                Reload Application
                            </Button>
                        </CardFooter>
                    </Card>
                </div>
            );
        }

        return this.props.children;
    }
}
