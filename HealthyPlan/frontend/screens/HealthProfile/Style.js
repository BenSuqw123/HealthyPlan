import { StyleSheet } from "react-native";

import { Colors, Radius, Spacing } from "../../configs/Theme";

export default StyleSheet.create({
    scroll: {padding: Spacing.medium, paddingBottom: 110},
    setupHeader: {marginBottom: Spacing.large},
    setupBadge: {alignSelf: "flex-start", marginBottom: 10, paddingHorizontal: 11, paddingVertical: 6, borderRadius: Radius.round, backgroundColor: Colors.primaryLight},
    setupBadgeText: {fontSize: 12, fontWeight: "700", color: Colors.primaryDark},
    title: {fontSize: 27, lineHeight: 34, fontWeight: "800", color: Colors.text},
    description: {marginTop: 8, fontSize: 14, lineHeight: 21, color: Colors.textSecondary},
    errorBox: {marginBottom: Spacing.medium, padding: 12, borderRadius: Radius.small, backgroundColor: "#FFF0F0"},
    errorText: {fontSize: 14, lineHeight: 20, color: Colors.error},
    section: {marginBottom: Spacing.medium},
    infoBox: {marginBottom: Spacing.medium, padding: 12, flexDirection: "row", borderRadius: Radius.small, backgroundColor: "#EFF6F2"},
    infoText: {flex: 1, marginLeft: 8, fontSize: 13, lineHeight: 19, color: Colors.textSecondary},
    issueRow: {paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: Colors.border},
    issueHeader: {flexDirection: "row", alignItems: "center"},
    issueName: {flex: 1, fontSize: 14, fontWeight: "600", color: Colors.text},
    issueParent: {marginTop: 3, fontSize: 12, color: Colors.textSecondary},
    selectedTag: {paddingHorizontal: 9, paddingVertical: 4, borderRadius: Radius.round, backgroundColor: Colors.primaryLight},
    selectedTagText: {fontSize: 11, fontWeight: "700", color: Colors.primaryDark},
    issuesError: {fontSize: 13, lineHeight: 19, color: Colors.error},
    retryText: {marginTop: 6, fontSize: 13, fontWeight: "700", color: Colors.primary},
    detailsScroll: {padding: Spacing.medium, paddingBottom: Spacing.huge},
    summaryCard: {marginBottom: Spacing.medium},
    summaryTop: {flexDirection: "row", alignItems: "center"},
    summaryIcon: {width: 56, height: 56, marginRight: 14, borderRadius: 18, alignItems: "center", justifyContent: "center", backgroundColor: Colors.primaryLight},
    summaryTitle: {fontSize: 19, fontWeight: "800", color: Colors.text},
    summaryText: {marginTop: 3, fontSize: 13, color: Colors.textSecondary},
    detailRow: {paddingVertical: 11, flexDirection: "row", alignItems: "flex-start", borderBottomWidth: 1, borderBottomColor: Colors.border},
    detailLabel: {flex: 1, paddingRight: 12, fontSize: 14, color: Colors.textSecondary},
    detailValue: {flex: 1.2, fontSize: 14, fontWeight: "600", textAlign: "right", color: Colors.text},
    issueChip: {alignSelf: "flex-start", marginRight: 7, marginBottom: 7, paddingHorizontal: 11, paddingVertical: 7, borderRadius: Radius.round, backgroundColor: Colors.primaryLight},
    issueChipText: {fontSize: 13, fontWeight: "600", color: Colors.primaryDark},
    emptyIssues: {fontSize: 14, color: Colors.textSecondary}
});
