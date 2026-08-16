import { StyleSheet, Text, View } from "react-native";

import { Colors, Radius } from "../configs/Theme";

const STATUS_STYLES = {
    success: {backgroundColor: "#E4F3EB", color: Colors.success},
    warning: {backgroundColor: "#FFF3DC", color: Colors.warning},
    error: {backgroundColor: "#FFF0F0", color: Colors.error},
    neutral: {backgroundColor: "#EEF2F0", color: Colors.textSecondary}
};

const StatusBadge = ({label, tone = "neutral"}) => {
    const statusStyle = STATUS_STYLES[tone] || STATUS_STYLES.neutral;

    return (
        <View style={[styles.badge, {backgroundColor: statusStyle.backgroundColor}]}>
            <Text style={[styles.text, {color: statusStyle.color}]}>{label}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    badge: {alignSelf: "flex-start", paddingHorizontal: 10, paddingVertical: 5, borderRadius: Radius.round},
    text: {fontSize: 11, fontWeight: "800"}
});

export default StatusBadge;
