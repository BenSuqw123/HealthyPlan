import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";

import { Colors, Radius, Spacing } from "../configs/Theme";

const ChoiceField = ({label, options, value, onChange, error, horizontal = false}) => {
    const content = options.map((option) => {
        const selected = option.value === value;

        return (
            <Pressable
                accessibilityRole="button"
                accessibilityState={{selected}}
                key={option.value}
                onPress={() => onChange(option.value)}
                style={[styles.choice, selected && styles.selectedChoice]}
            >
                <Text style={[styles.choiceText, selected && styles.selectedText]}>{option.label}</Text>
            </Pressable>
        );
    });

    return (
        <View style={styles.wrapper}>
            {label && <Text style={styles.label}>{label}</Text>}
            {horizontal ? (
                <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.row}>{content}</ScrollView>
            ) : (
                <View style={styles.wrap}>{content}</View>
            )}
            {error && <Text style={styles.error}>{error}</Text>}
        </View>
    );
}

const styles = StyleSheet.create({
    wrapper: {marginBottom: Spacing.medium},
    label: {marginBottom: 7, fontSize: 14, fontWeight: "600", color: Colors.text},
    row: {paddingRight: Spacing.medium},
    wrap: {flexDirection: "row", flexWrap: "wrap"},
    choice: {minHeight: 42, marginRight: 8, marginBottom: 8, paddingHorizontal: 14, borderRadius: Radius.round, borderWidth: 1, borderColor: Colors.border, alignItems: "center", justifyContent: "center", backgroundColor: Colors.surface},
    selectedChoice: {borderColor: Colors.primary, backgroundColor: Colors.primaryLight},
    choiceText: {fontSize: 14, color: Colors.textSecondary},
    selectedText: {fontWeight: "700", color: Colors.primaryDark},
    error: {marginTop: 2, fontSize: 13, color: Colors.error}
});

export default ChoiceField;
