export type LLMProviderType = 'anthropic' | 'openai' | 'google' | 'xai' | 'perplexity' | 'mock';

export interface LLMConfig {
    provider: LLMProviderType;
    model_name: string;
    is_active: boolean;
    api_key_masked?: string | null;
}

export interface LLMConfigUpdate {
    provider?: LLMProviderType;
    model_name?: string;
    api_key?: string;
    is_active?: boolean;
}
