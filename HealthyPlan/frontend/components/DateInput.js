import { useMemo, useState } from "react";
import { Modal, Pressable, StyleSheet, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "./AppButton";
import { Colors, Radius, Shadow, Spacing } from "../configs/Theme";

const WEEK_DAYS = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];

const parseDate = (value) => {
    if (!value) {
        return new Date();
    }

    const [year, month, day] = value.split("-").map(Number);
    return new Date(year, month - 1, day);
}

const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

const getCalendarDays = (viewDate) => {
    const year = viewDate.getFullYear();
    const month = viewDate.getMonth();
    const firstWeekDay = (new Date(year, month, 1).getDay() + 6) % 7;
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const days = Array.from({length: firstWeekDay}, (_, index) => ({key: `blank-${index}`, date: null}));

    for (let day = 1; day <= daysInMonth; day += 1) {
        const date = new Date(year, month, day);
        days.push({key: formatDate(date), date});
    }

    return days;
}

const DateInput = ({label, value, onChange, error, minimumDate, maximumDate}) => {
    const [visible, setVisible] = useState(false);
    const [selectedDate, setSelectedDate] = useState(parseDate(value));
    const [viewDate, setViewDate] = useState(parseDate(value));
    const calendarDays = useMemo(() => getCalendarDays(viewDate), [viewDate]);

    const openCalendar = () => {
        const currentDate = parseDate(value);
        setSelectedDate(currentDate);
        setViewDate(currentDate);
        setVisible(true);
    }

    const changeMonth = (amount) => {
        setViewDate(new Date(viewDate.getFullYear(), viewDate.getMonth() + amount, 1));
    }

    const isDisabled = (date) => {
        const formatted = formatDate(date);
        return (minimumDate && formatted < minimumDate) || (maximumDate && formatted > maximumDate);
    }

    const confirmDate = () => {
        onChange(formatDate(selectedDate));
        setVisible(false);
    }

    return (
        <View style={styles.wrapper}>
            {label && <Text style={styles.label}>{label}</Text>}
            <Pressable accessibilityRole="button" onPress={openCalendar} style={[styles.input, error && styles.errorBorder]}>
                <Ionicons name="calendar-outline" size={20} color={Colors.primary} />
                <Text style={[styles.value, !value && styles.placeholder]}>{value || "Chọn ngày"}</Text>
                <Ionicons name="chevron-down" size={18} color={Colors.textSecondary} />
            </Pressable>
            {error && <Text style={styles.error}>{error}</Text>}

            <Modal animationType="fade" transparent visible={visible} onRequestClose={() => setVisible(false)}>
                <View style={styles.overlay}>
                    <View style={styles.modal}>
                        <View style={styles.monthHeader}>
                            <View style={styles.arrowGroup}>
                                <Pressable accessibilityLabel="Năm trước" hitSlop={6} onPress={() => changeMonth(-12)} style={styles.arrowButton}>
                                    <Ionicons name="play-back" size={18} color={Colors.primary} />
                                </Pressable>
                                <Pressable accessibilityLabel="Tháng trước" hitSlop={6} onPress={() => changeMonth(-1)} style={styles.arrowButton}>
                                    <Ionicons name="chevron-back" size={22} color={Colors.primary} />
                                </Pressable>
                            </View>
                            <Text style={styles.monthTitle}>Tháng {viewDate.getMonth() + 1}, {viewDate.getFullYear()}</Text>
                            <View style={styles.arrowGroup}>
                                <Pressable accessibilityLabel="Tháng sau" hitSlop={6} onPress={() => changeMonth(1)} style={styles.arrowButton}>
                                    <Ionicons name="chevron-forward" size={22} color={Colors.primary} />
                                </Pressable>
                                <Pressable accessibilityLabel="Năm sau" hitSlop={6} onPress={() => changeMonth(12)} style={styles.arrowButton}>
                                    <Ionicons name="play-forward" size={18} color={Colors.primary} />
                                </Pressable>
                            </View>
                        </View>
                        <View style={styles.weekRow}>
                            {WEEK_DAYS.map((day) => <Text key={day} style={styles.weekDay}>{day}</Text>)}
                        </View>
                        <View style={styles.daysGrid}>
                            {calendarDays.map((item) => {
                                if (!item.date) {
                                    return <View key={item.key} style={styles.dayCell} />;
                                }

                                const selected = formatDate(item.date) === formatDate(selectedDate);
                                const disabled = isDisabled(item.date);
                                return (
                                    <Pressable key={item.key} disabled={disabled} onPress={() => setSelectedDate(item.date)} style={[styles.dayCell, selected && styles.selectedDay]}>
                                        <Text style={[styles.dayText, selected && styles.selectedDayText, disabled && styles.disabledDay]}>{item.date.getDate()}</Text>
                                    </Pressable>
                                );
                            })}
                        </View>
                        <View style={styles.actions}>
                            <AppButton title="Hủy" variant="outline" onPress={() => setVisible(false)} style={styles.actionButton} />
                            <AppButton title="Chọn ngày" onPress={confirmDate} style={styles.actionButton} />
                        </View>
                    </View>
                </View>
            </Modal>
        </View>
    );
}

const styles = StyleSheet.create({
    wrapper: {marginBottom: Spacing.medium},
    label: {marginBottom: 7, fontSize: 14, fontWeight: "600", color: Colors.text},
    input: {minHeight: 50, paddingHorizontal: 14, flexDirection: "row", alignItems: "center", borderWidth: 1, borderColor: Colors.border, borderRadius: Radius.medium, backgroundColor: Colors.surface},
    value: {flex: 1, marginHorizontal: 10, fontSize: 16, color: Colors.text},
    placeholder: {color: Colors.disabled},
    errorBorder: {borderColor: Colors.error},
    error: {marginTop: 5, fontSize: 13, color: Colors.error},
    overlay: {flex: 1, padding: Spacing.medium, alignItems: "center", justifyContent: "center", backgroundColor: Colors.overlay},
    modal: {width: "100%", maxWidth: 390, padding: Spacing.medium, borderRadius: Radius.large, backgroundColor: Colors.surface, ...Shadow},
    monthHeader: {flexDirection: "row", alignItems: "center", justifyContent: "space-between"},
    arrowGroup: {flexDirection: "row"},
    arrowButton: {width: 32, height: 42, alignItems: "center", justifyContent: "center"},
    monthTitle: {fontSize: 17, fontWeight: "700", color: Colors.text},
    weekRow: {marginTop: 10, flexDirection: "row"},
    weekDay: {width: "14.2857%", paddingVertical: 8, textAlign: "center", fontSize: 12, fontWeight: "700", color: Colors.textSecondary},
    daysGrid: {flexDirection: "row", flexWrap: "wrap"},
    dayCell: {width: "14.2857%", aspectRatio: 1, alignItems: "center", justifyContent: "center", borderRadius: Radius.round},
    selectedDay: {backgroundColor: Colors.primary},
    dayText: {fontSize: 14, color: Colors.text},
    selectedDayText: {fontWeight: "700", color: Colors.surface},
    disabledDay: {color: Colors.border},
    actions: {marginTop: Spacing.medium, flexDirection: "row"},
    actionButton: {flex: 1, marginHorizontal: 4}
});

export default DateInput;
