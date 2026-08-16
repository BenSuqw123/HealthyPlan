import { StyleSheet } from "react-native";

import { Colors, Radius, Spacing } from "../../configs/Theme";

export default StyleSheet.create({
    authScroll: {flexGrow: 1, paddingHorizontal: Spacing.large, paddingVertical: Spacing.large, justifyContent: "center"},
    brand: {alignItems: "center", marginBottom: Spacing.large},
    brandIcon: {width: 72, height: 72, borderRadius: 24, alignItems: "center", justifyContent: "center", backgroundColor: Colors.primary},
    brandName: {marginTop: 14, fontSize: 28, fontWeight: "800", color: Colors.text},
    subtitle: {marginTop: 6, fontSize: 15, lineHeight: 21, textAlign: "center", color: Colors.textSecondary},
    formCard: {padding: Spacing.large, borderWidth: 1, borderColor: Colors.border, borderRadius: Radius.large, backgroundColor: Colors.surface},
    formTitle: {fontSize: 22, fontWeight: "800", color: Colors.text},
    formDescription: {marginTop: 6, marginBottom: Spacing.large, fontSize: 14, lineHeight: 20, color: Colors.textSecondary},
    generalError: {marginBottom: Spacing.medium, padding: 12, borderRadius: Radius.small, backgroundColor: "#FFF0F0", fontSize: 14, lineHeight: 20, color: Colors.error},
    footerRow: {marginTop: Spacing.large, flexDirection: "row", alignItems: "center", justifyContent: "center"},
    footerText: {fontSize: 14, color: Colors.textSecondary},
    footerLink: {padding: 8, fontSize: 14, fontWeight: "700", color: Colors.primary},
    profileHeader: {padding: Spacing.large, alignItems: "center", backgroundColor: Colors.primary},
    avatar: {width: 76, height: 76, borderRadius: 38, alignItems: "center", justifyContent: "center", backgroundColor: Colors.surface},
    profileName: {marginTop: 12, fontSize: 22, fontWeight: "800", color: Colors.surface},
    profileUsername: {marginTop: 3, fontSize: 14, color: "#D9F1E6"},
    content: {padding: Spacing.medium},
    cardSpacing: {marginBottom: Spacing.medium},
    infoRow: {paddingVertical: 10, flexDirection: "row", alignItems: "center"},
    infoIcon: {width: 32},
    infoContent: {flex: 1},
    infoLabel: {fontSize: 12, color: Colors.textSecondary},
    infoValue: {marginTop: 2, fontSize: 15, fontWeight: "600", color: Colors.text},
    actionButton: {marginTop: Spacing.small},
    updateScroll: {padding: Spacing.medium, paddingBottom: Spacing.huge}
});
