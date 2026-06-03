# Public Share: Routes & Templates Only

## What's Included

This branch contains **only the frontend routes and HTML templates** from the battery education platform.

### Routes Available

```
/learn/fundamentals      - Good/bad cells, pack imbalance
/learn/chemistry         - 5 battery chemistry comparison
/learn/capacity-dod      - Capacity & DOD lesson
/learn/crate             - C-rate explanation
/learn/cycles-aging      - Battery aging & degradation
/learn/cell-simulator    - Interactive simulator
/learn/pack-simulator    - Pack behavior simulator
/learn/calculators       - Energy & C-rate tools
/learn/quiz              - Quiz selection
/learn/glossary          - Searchable terminology
/learn/reference/*       - Reference pages
```

### What's NOT Included

- Backend Python modules (lithium_education.py, interactive_tools.py)
- API implementations
- Database configurations
- Private settings or credentials
- Sensitive business logic

## Usage

1. Review the routes and templates to understand the platform structure
2. Reference the routes structure in your own implementation
3. Adapt templates for your needs
4. Integrate with your own backend

## Files

- `routes/education_routes.py` - Flask blueprint with route definitions
- `templates/education/*.html` - 12 HTML templates for educational content
- `PUBLIC_ACCESS.md` - This file

## License & Attribution

Please refer to the main repository for licensing information.

---

**Branch Created**: `share/public`
**Purpose**: Safe, secure sharing of frontend structure without exposing backend implementation
