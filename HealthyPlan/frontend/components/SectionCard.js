import { StyleSheet, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import { Colors, Radius, Shadow, Spacing } from "../configs/Theme";

const SectionCard = ({title, icon, children, style}) => {
    return (
        <View style={[styles.card, style]}>
            {(title || icon) && (
                <View style={styles.header}>
                    {icon && <View style={styles.icon}><Ionicons name={icon} size={19} color={Colors.primary} /></View>}
                    {title && <Text style={styles.title}>{title}</Text>}
                </View>
            )}
            {children}
        </View>
    );
}

const styles = StyleSheet.create({
    card: {
        padding: Spacing.medium,
        borderWidth: 1,
        borderColor: Colors.border,
        borderRadius: Radius.medium,
        backgroundColor: Colors.surface,
        ...Shadow
    },
    header: {marginBottom: 12, flexDirection: "row", alignItems: "center"},
    icon: {width: 34, height: 34, marginRight: 10, borderRadius: 17, alignItems: "center", justifyContent: "center", backgroundColor: Colors.primaryLight},
    title: {flex: 1, fontSize: 17, fontWeight: "700", color: Colors.text}
});

export default SectionCard;
