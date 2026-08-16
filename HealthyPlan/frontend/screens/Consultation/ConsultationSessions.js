import { useCallback, useState } from "react";
import { Alert, FlatList, Modal, Pressable, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import { useFocusEffect } from "@react-navigation/native";

import AppButton from "../../components/AppButton";
import AppTextInput from "../../components/AppTextInput";
import ScreenContainer from "../../components/ScreenContainer";
import { EmptyView, ErrorView, LoadingView } from "../../components/StateViews";
import Apis, { endpoints, getErrorMessage, getFieldError, requireResponseData } from "../../configs/Apis";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const ConsultationSessions = ({navigation}) => {
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [editingSession, setEditingSession] = useState(null);
    const [title, setTitle] = useState("");
    const [titleError, setTitleError] = useState("");
    const [savingTitle, setSavingTitle] = useState(false);

    const loadSessions = async (refresh = false) => {
        try {
            refresh ? setRefreshing(true) : setLoading(true);
            setErrorMessage("");
            const response = await Apis.get(endpoints.consultationSessions);
            setSessions(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    }

    useFocusEffect(useCallback(() => {
        loadSessions();
    }, []));

    const openRename = (session) => {
        setEditingSession(session);
        setTitle(session.title || "");
        setTitleError("");
    }

    const renameSession = async () => {
        if (!title.trim()) {
            setTitleError("Tiêu đề không được để trống.");
            return;
        }

        try {
            setSavingTitle(true);
            const response = await Apis.patch(endpoints.consultationSession(editingSession.id), {title: title.trim()});
            const updatedSession = requireResponseData(response, "Máy chủ không trả về cuộc tư vấn đã cập nhật.");
            setSessions((current) => current.map((session) => session.id === updatedSession.id ? updatedSession : session));
            setEditingSession(null);
        } catch (error) {
            setTitleError(getFieldError(error, "title") || getErrorMessage(error));
        } finally {
            setSavingTitle(false);
        }
    }

    const deleteSession = async (sessionId) => {
        try {
            await Apis.delete(endpoints.consultationSession(sessionId));
            setSessions((current) => current.filter((session) => session.id !== sessionId));
        } catch (error) {
            Alert.alert("Không thể xóa", getErrorMessage(error));
        }
    }

    const confirmDelete = (session) => {
        Alert.alert("Xóa cuộc tư vấn", `Bạn có chắc muốn xóa “${session.title || "Cuộc tư vấn"}”?`, [
            {text: "Hủy", style: "cancel"},
            {text: "Xóa", style: "destructive", onPress: () => deleteSession(session.id)}
        ]);
    }

    const renderSession = ({item}) => (
        <View style={styles.sessionCard}>
            <Pressable accessibilityRole="button" onPress={() => navigation.navigate("ConsultationChat", {sessionId: item.id, title: item.title})} style={{flex: 1, flexDirection: "row", alignItems: "center"}}>
                <View style={styles.sessionIcon}><Ionicons name="chatbubble-ellipses-outline" size={22} color={Colors.primary} /></View>
                <View style={styles.sessionMain}>
                    <Text numberOfLines={2} style={styles.sessionTitle}>{item.title || "Cuộc tư vấn sức khỏe"}</Text>
                    <Text style={styles.sessionDate}>{new Date(item.updated_at).toLocaleString("vi-VN")}</Text>
                </View>
            </Pressable>
            <Pressable accessibilityLabel="Đổi tên cuộc tư vấn" onPress={() => openRename(item)} style={styles.iconButton}><Ionicons name="create-outline" size={20} color={Colors.textSecondary} /></Pressable>
            <Pressable accessibilityLabel="Xóa cuộc tư vấn" onPress={() => confirmDelete(item)} style={styles.iconButton}><Ionicons name="trash-outline" size={19} color={Colors.error} /></Pressable>
        </View>
    );

    if (loading && sessions.length === 0) return <ScreenContainer><LoadingView message="Đang tải các cuộc tư vấn..." /></ScreenContainer>;
    if (errorMessage && sessions.length === 0) return <ScreenContainer><ErrorView message={errorMessage} onRetry={loadSessions} /></ScreenContainer>;

    return (
        <ScreenContainer>
            <FlatList
                data={sessions}
                keyExtractor={(item) => item.id}
                renderItem={renderSession}
                refreshing={refreshing}
                onRefresh={() => loadSessions(true)}
                contentContainerStyle={[styles.list, sessions.length === 0 && {flex: 1}]}
                ListHeaderComponent={
                    <View style={styles.header}>
                        <View style={styles.titleRow}>
                            <View style={styles.titleBlock}><Text style={styles.title}>Tư vấn sức khỏe</Text><Text style={styles.subtitle}>Trao đổi với trợ lý sử dụng hồ sơ sức khỏe và tài liệu tham khảo.</Text></View>
                            <Pressable accessibilityLabel="Tạo cuộc tư vấn" onPress={() => navigation.navigate("ConsultationChat")} style={styles.newButton}><Ionicons name="add" size={27} color={Colors.surface} /></Pressable>
                        </View>
                    </View>
                }
                ListEmptyComponent={<EmptyView icon="chatbubbles-outline" title="Chưa có cuộc tư vấn" message="Bắt đầu bằng một câu hỏi về sức khỏe hoặc dinh dưỡng." actionTitle="Bắt đầu tư vấn" onAction={() => navigation.navigate("ConsultationChat")} />}
            />

            <Modal animationType="fade" transparent visible={Boolean(editingSession)} onRequestClose={() => setEditingSession(null)}>
                <View style={styles.modalOverlay}>
                    <View style={styles.modal}>
                        <Text style={styles.modalTitle}>Đổi tên cuộc tư vấn</Text>
                        <Text style={styles.modalDescription}>Một tiêu đề ngắn sẽ giúp bạn tìm lại nội dung dễ hơn.</Text>
                        <AppTextInput autoFocus error={titleError} maxLength={255} value={title} onChangeText={(value) => {setTitle(value); setTitleError("");}} />
                        <View style={styles.modalActions}>
                            <AppButton title="Hủy" variant="outline" onPress={() => setEditingSession(null)} style={styles.modalButton} />
                            <AppButton title="Lưu" loading={savingTitle} onPress={renameSession} style={styles.modalButton} />
                        </View>
                    </View>
                </View>
            </Modal>
        </ScreenContainer>
    );
}

export default ConsultationSessions;
