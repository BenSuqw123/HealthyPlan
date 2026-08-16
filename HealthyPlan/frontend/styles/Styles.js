import { StyleSheet } from "react-native";

import { Colors, Radius, Shadow, Spacing } from "../configs/Theme";

export default StyleSheet.create({
    flex: {flex: 1},
    row: {flexDirection: "row", alignItems: "center"},
    rowBetween: {flexDirection: "row", alignItems: "center", justifyContent: "space-between"},
    wrap: {flexDirection: "row", flexWrap: "wrap"},
    screenPadding: {paddingHorizontal: Spacing.medium},
    title: {fontSize: 28, lineHeight: 34, fontWeight: "800", color: Colors.text},
    heading: {fontSize: 20, lineHeight: 26, fontWeight: "700", color: Colors.text},
    subheading: {fontSize: 16, lineHeight: 22, fontWeight: "600", color: Colors.text},
    body: {fontSize: 15, lineHeight: 22, color: Colors.text},
    muted: {fontSize: 14, lineHeight: 20, color: Colors.textSecondary},
    card: {
        padding: Spacing.medium,
        borderRadius: Radius.medium,
        borderWidth: 1,
        borderColor: Colors.border,
        backgroundColor: Colors.surface,
        ...Shadow
    },
    separator: {height: 1, backgroundColor: Colors.border},
    marginTopSmall: {marginTop: Spacing.small},
    marginTopMedium: {marginTop: Spacing.medium},
    marginBottomMedium: {marginBottom: Spacing.medium}
});
