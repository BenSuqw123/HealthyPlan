import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import { Colors, Radius, Spacing } from "../configs/Theme";

const AppTextInput = ({label, error, secureTextEntry = false, icon, multiline = false, inputStyle, ...props}) => {
    const [passwordHidden, setPasswordHidden] = useState(secureTextEntry);

    return (
        <View style={styles.wrapper}>
            {label && <Text style={styles.label}>{label}</Text>}
            <View style={[styles.inputContainer, multiline && styles.multilineContainer, error && styles.errorBorder]}>
                {icon && <Ionicons name={icon} size={20} color={Colors.textSecondary} style={styles.leftIcon} />}
                <TextInput
                    {...props}
                    multiline={multiline}
                    placeholderTextColor={Colors.disabled}
                    secureTextEntry={passwordHidden}
                    style={[styles.input, multiline && styles.multilineInput, inputStyle]}
                />
                {secureTextEntry && (
                    <Pressable
                        accessibilityRole="button"
                        accessibilityLabel={passwordHidden ? "Hiện mật khẩu" : "Ẩn mật khẩu"}
                        hitSlop={10}
                        onPress={() => setPasswordHidden(!passwordHidden)}
                    >
                        <Ionicons name={passwordHidden ? "eye-outline" : "eye-off-outline"} size={21} color={Colors.textSecondary} />
                    </Pressable>
                )}
            </View>
            {error && <Text style={styles.error}>{error}</Text>}
        </View>
    );
}

const styles = StyleSheet.create({
    wrapper: {marginBottom: Spacing.medium},
    label: {marginBottom: 7, fontSize: 14, fontWeight: "600", color: Colors.text},
    inputContainer: {
        minHeight: 50,
        paddingHorizontal: 14,
        flexDirection: "row",
        alignItems: "center",
        borderWidth: 1,
        borderColor: Colors.border,
        borderRadius: Radius.medium,
        backgroundColor: Colors.surface
    },
    multilineContainer: {alignItems: "flex-start", minHeight: 110, paddingTop: 12},
    input: {flex: 1, paddingVertical: 10, fontSize: 16, color: Colors.text},
    multilineInput: {minHeight: 84, textAlignVertical: "top"},
    leftIcon: {marginRight: Spacing.small},
    errorBorder: {borderColor: Colors.error},
    error: {marginTop: 5, fontSize: 13, color: Colors.error}
});

export default AppTextInput;
