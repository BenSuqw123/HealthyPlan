import { ActivityIndicator, StyleSheet, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "./AppButton";
import { Colors, Spacing } from "../configs/Theme";

export const LoadingView = ({message = "Đang tải dữ liệu..."}) => {
    return (
        <View style={styles.container}>
            <ActivityIndicator size="large" color={Colors.primary} />
            <Text style={styles.message}>{message}</Text>
        </View>
    );
}

export const ErrorView = ({message, onRetry}) => {
    return (
        <View style={styles.container}>
            <View style={[styles.iconCircle, styles.errorCircle]}>
                <Ionicons name="alert-circle-outline" size={34} color={Colors.error} />
            </View>
            <Text style={styles.title}>Chưa thể tải dữ liệu</Text>
            <Text style={styles.message}>{message}</Text>
            {onRetry && <AppButton title="Thử lại" icon="refresh-outline" variant="secondary" onPress={onRetry} style={styles.button} />}
        </View>
    );
}

export const EmptyView = ({title, message, icon = "leaf-outline", actionTitle, onAction}) => {
    return (
        <View style={styles.container}>
            <View style={styles.iconCircle}>
                <Ionicons name={icon} size={34} color={Colors.primary} />
            </View>
            <Text style={styles.title}>{title}</Text>
            <Text style={styles.message}>{message}</Text>
            {actionTitle && onAction && <AppButton title={actionTitle} onPress={onAction} style={styles.button} />}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {flex: 1, padding: Spacing.large, alignItems: "center", justifyContent: "center"},
    iconCircle: {width: 68, height: 68, borderRadius: 34, alignItems: "center", justifyContent: "center", backgroundColor: Colors.primaryLight},
    errorCircle: {backgroundColor: "#FFF0F0"},
    title: {marginTop: Spacing.medium, fontSize: 18, fontWeight: "700", textAlign: "center", color: Colors.text},
    message: {marginTop: Spacing.small, maxWidth: 320, fontSize: 14, lineHeight: 21, textAlign: "center", color: Colors.textSecondary},
    button: {marginTop: Spacing.large, minWidth: 150}
});
