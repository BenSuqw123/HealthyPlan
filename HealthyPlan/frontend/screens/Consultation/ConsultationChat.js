import { useEffect, useRef, useState } from "react";
import { ActivityIndicator, FlatList, KeyboardAvoidingView, Platform, Pressable, Text, TextInput, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import ScreenContainer from "../../components/ScreenContainer";
import { ErrorView, LoadingView } from "../../components/StateViews";
import Apis, { endpoints, getErrorMessage, requireResponseData } from "../../configs/Apis";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const ConsultationChat = ({navigation, route}) => {
    const [sessionId, setSessionId] = useState(route.params?.sessionId || null);
    const [messages, setMessages] = useState([]);
    const [content, setContent] = useState("");
    const [loading, setLoading] = useState(Boolean(route.params?.sessionId));
    const [waiting, setWaiting] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const listRef = useRef(null);

    const loadMessages = async () => {
        if (!sessionId) return;

        try {
            setLoading(true);
            setErrorMessage("");
            const response = await Apis.get(endpoints.consultationMessages(sessionId));
            setMessages(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        navigation.setOptions({title: route.params?.title || "Tư vấn sức khỏe"});
        loadMessages();
    }, []);

    const sendMessage = async () => {
        const message = content.trim();
        if (!message || waiting) return;

        const temporaryMessage = {id: `temporary-${Date.now()}`, role: "user", content: message};
        setMessages((current) => [...current, temporaryMessage]);
        setContent("");
        setErrorMessage("");

        try {
            setWaiting(true);
            const payload = {message};
            if (sessionId) payload.session_id = sessionId;
            const response = await Apis.post(endpoints.consultations, payload, {timeout: 180000});
            const assistantMessage = requireResponseData(response, "Máy chủ không trả về câu trả lời tư vấn.");
            if (!assistantMessage.id || !assistantMessage.session || assistantMessage.role !== "assistant" || !assistantMessage.content) {
                const error = new Error("Phản hồi tư vấn chưa đầy đủ.");
                error.userMessage = error.message;
                throw error;
            }
            if (!sessionId) setSessionId(assistantMessage.session);
            setMessages((current) => [...current, assistantMessage]);
        } catch (error) {
            setMessages((current) => current.filter((item) => item.id !== temporaryMessage.id));
            setContent(message);
            setErrorMessage(getErrorMessage(error));
        } finally {
            setWaiting(false);
        }
    }

    const renderMessage = ({item}) => {
        const isUser = item.role === "user";
        return (
            <View style={[styles.messageRow, isUser ? styles.userRow : styles.assistantRow]}>
                <View style={[styles.bubble, isUser ? styles.userBubble : styles.assistantBubble]}>
                    <Text selectable style={[styles.messageText, isUser ? styles.userText : styles.assistantText]}>{item.content}</Text>
                </View>
            </View>
        );
    }

    if (loading) return <ScreenContainer withHeader><LoadingView message="Đang tải cuộc trò chuyện..." /></ScreenContainer>;
    if (errorMessage && messages.length === 0 && sessionId) return <ScreenContainer withHeader><ErrorView message={errorMessage} onRetry={loadMessages} /></ScreenContainer>;

    return (
        <ScreenContainer withHeader>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} keyboardVerticalOffset={Platform.OS === "ios" ? 90 : 0} style={styles.chat}>
                <FlatList
                    ref={listRef}
                    data={messages}
                    keyExtractor={(item) => String(item.id)}
                    renderItem={renderMessage}
                    contentContainerStyle={[styles.messageList, messages.length === 0 && {flexGrow: 1}]}
                    keyboardShouldPersistTaps="handled"
                    onContentSizeChange={() => listRef.current?.scrollToEnd({animated: true})}
                    ListEmptyComponent={
                        <View style={styles.emptyChat}>
                            <View style={styles.emptyIcon}><Ionicons name="chatbubbles-outline" size={34} color={Colors.primary} /></View>
                            <Text style={styles.emptyTitle}>Bạn muốn hỏi điều gì?</Text>
                            <Text style={styles.emptyText}>Hãy mô tả câu hỏi sức khỏe hoặc dinh dưỡng. Trợ lý sẽ dựa trên hồ sơ hiện tại để trả lời.</Text>
                        </View>
                    }
                    ListFooterComponent={waiting ? <View style={[styles.messageRow, styles.assistantRow]}><View style={[styles.bubble, styles.assistantBubble, styles.waitingBubble]}><ActivityIndicator color={Colors.primary} /></View></View> : null}
                />
                <View style={styles.composerArea}>
                    {errorMessage ? <Text style={styles.chatError}>{errorMessage}</Text> : null}
                    <View style={styles.composer}>
                        <TextInput
                            multiline
                            maxLength={2000}
                            editable={!waiting}
                            onChangeText={setContent}
                            placeholder="Nhập câu hỏi của bạn..."
                            placeholderTextColor={Colors.disabled}
                            style={styles.inputBox}
                            value={content}
                        />
                        <Pressable accessibilityLabel="Gửi câu hỏi" disabled={waiting || !content.trim()} onPress={sendMessage} style={[styles.sendButton, (waiting || !content.trim()) && styles.disabledSend]}>
                            {waiting ? <ActivityIndicator color={Colors.surface} /> : <Ionicons name="send" size={21} color={Colors.surface} />}
                        </Pressable>
                    </View>
                    <Text style={styles.safetyText}>Thông tin tư vấn không thay thế chẩn đoán hoặc điều trị của nhân viên y tế.</Text>
                </View>
            </KeyboardAvoidingView>
        </ScreenContainer>
    );
}

export default ConsultationChat;
